#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import os, sys
import argparse
import glob



def get_parser():
	
	parser = argparse.ArgumentParser(description='Find SNPs in VCF files based on a tab file of SNP typing')
	
	parser.add_argument('-i', action="store", dest='vcf',
						 required=True, help='VCF file (REQUIRED)')
	
	parser.add_argument('-t', action="store", dest='tab',
						type=str, required=True, help='tab file (REQUIRED)')

	parser.add_argument("-m", "--mode", dest='mode', action="store_true", help="use multi vcf mode")
	

	return parser
	

def tab_typing_reader(tab_file):

	dico_SNP = {}

	f = open(tab_file, 'r')
	lines = f.readlines()
	f.close()
	
	header = True
	for line in lines :
		if header :
			header = False
			continue
		line = line.rstrip().split('\t')
		chr = line[0]
		pos = line[1]
		nucl = line[4]
		if chr not in dico_SNP :
			dico_SNP[chr] = {}
		dico_SNP[chr][pos] = nucl
		
	return dico_SNP
	

def vcf_parser(vcf_file,dico):

	f = open(vcf_file)
	lines = f.readlines()
	f.close()
	
	sum = 0
	
	for line in lines :
		if line[0] == '#':
			continue
		line = line.rstrip().split('\t')
		chr = line[0]
		pos = line[1]
		nucl = line[4]
		
		if chr in dico :
			if pos in dico[chr] :
				if nucl == dico[chr][pos] :
					sum += 1
					
	nb_SNP_dico = 0
	for chr in dico:
		nb_SNP_dico += len(dico[chr])
			
	prc = float(float(sum)/float(nb_SNP_dico))*100
	
	return str(prc)

	
def vcf_parser_multi(vcf_file,dico):

	file = open(vcf_file,'r')
	lines = file.readlines()
	file.close()
	
	for line in lines :
		if line[0:2] == '##':
			continue
		elif line[0:2] == '#C':
			line = line.rstrip().split('\t')
			genome_order = line[9:]
			dico_sum = {}
			for genome in genome_order:
				dico_sum[genome] = 0
		else:
		
			#print(line)
		
			line = line.rstrip().split('\t')
			chr = line[0]
			pos = line[1]
			ref = line[3]
			alt = line[4]
			
			
			
			if chr in dico :
				if pos in dico[chr]:
					#print(f'SEARCH --> {chr}:{pos}:{dico[chr][pos]}')
					i = 0
					for g in line[9:] :
						genotype = g.split(':')[0]
						if genotype == '0':
							var = ref
						elif genotype == '.':
							var = "."
						else :
							var = alt.split(',')[int(genotype)-1]
						#print(var)	
						if var == dico[chr][pos] :
							dico_sum[genome_order[i]] += 1
							#print(f'{chr}:{pos}:{dico[chr][pos]}')
							#print("found!")
						i+=1

						
	#print(dico_sum)
	n = 0
	for chr in dico :
		for pos in dico[chr]:
			n+=1
			
	for element in dico_sum :
		dico_sum[element] = float(float(dico_sum[element])/float(n))*100

	return dico_sum

	
#main function	
def main():

	# Get arguments 
	parser=get_parser()
	# Print parser.help if no arguments
	if len(sys.argv)==1:
		parser.print_help()
		sys.exit(1)
	
	Arguments=parser.parse_args()
	
	if Arguments.mode:
		dico = tab_typing_reader(Arguments.tab)
		#print(dico)
		dico_prc = vcf_parser_multi(Arguments.vcf,dico)
		for element in dico_prc:
			#print(f'{element}\t{dico_prc[element]}%')
			print(f'{element}\t{dico_prc[element]}')
	
	else:
	
		files = glob.glob(Arguments.vcf)
		
		for file in files :

			dico = tab_typing_reader(Arguments.tab)
			prc = vcf_parser(file,dico)
			print(f'{file}\t{Arguments.tab}\t{prc}%')
		


if __name__ == "__main__":
	main()	