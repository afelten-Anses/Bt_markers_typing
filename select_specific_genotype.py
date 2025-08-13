#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
import os, sys, time
import argparse

##################################
#####  Arguments definition  #####
##################################


def get_parser():

	parser = argparse.ArgumentParser(description='Select SNPs from a VCF file based on a list of genome IDs')

	parser.add_argument('-i', action="store", dest='vcf', 
						type=str, required=True,
						help='vcf file (REQUIRED)')

	parser.add_argument('-g', action="store", dest='genome_id', 
                     nargs='+', required=True , help='list of id genomes (REQUIRED)')
		                

	return parser


def read_vcf(vcf_file,genome_ids):

	file = open(vcf_file,'r')
	lines = file.readlines()
	file.close()
	
	print(f'chr\tpos\tref\talt\tgenotype')
	
	for line in lines :
		if line[0:2] == '##':
			continue
		elif line[0:2] == '#C':
			line = line.rstrip().split('\t')
			genome_order = line[9:]
		else:
			line = line.rstrip().split('\t')
			chr = line[0]
			pos = line[1]
			ref = line[3]
			alt = line[4]
			g = same_genotype(genome_ids,genome_order,line[9:])
			if g != False :
				g = int(g)
				if g == 0 :
					genotype = ref
				else :
					alt_list = alt.split(',')
					genotype = alt_list[g-1]
				print(f'{chr}\t{pos}\t{ref}\t{alt}\t{genotype}')	

	return 


def same_genotype(genome_ids,genome_order,line):

	genome_ids_index = []
	for element in genome_ids :
		genome_ids_index.append(genome_order.index(element))
		
	i = 0	
	other_genotype = []
	interest_genotype = ''
	genotype_list = []
	for element in line :	
		genotype = element.split(':')[0]
		#print(genotype)
		if i in genome_ids_index :
			if genotype == '.':
				return False
			if interest_genotype == '':
				interest_genotype = genotype
			elif genotype!=interest_genotype:
				return False
		else:
			if genotype == interest_genotype:
				return False
			genotype_list.append(genotype)
	
		#print(genotype_list)
		i+=1
		
	if interest_genotype in genotype_list :
		return False	
		
	return 	interest_genotype
		

###########################
#####  Main function  #####
###########################


def main():

	##################### gets arguments #####################

	parser=get_parser()
	
	#print parser.help if no arguments
	if len(sys.argv)==1:
		parser.print_help()
		sys.exit(1)
	
	# mettre tout les arguments dans la variable Argument
	Arguments=parser.parse_args()
	
	read_vcf(Arguments.vcf,Arguments.genome_id)
	
	
# lancer la fonction main()  au lancement du script
if __name__ == "__main__":
	main()	 	