#.csv function, pulls csv files from the Taxol-Biosynthetic-Pathway folder and organizes them into the Taxol-predicted-genes file

# open the filehandle for writing the output to
# this will be used when going through the PSI file
#

pg_filehandle = open('Taxol-predicted-genes','w')

def shout(x):   #start of the function, we defined and called the function shout
    x = x.upper()   #uppercases the output of the function
    print(x)    #prints the output


import os       #Import operating system

cwd = os.getcwd()  # Get the current working directory (cwd)
files = os.listdir(cwd)  # Get all the files in that directory

for file in os.listdir(cwd):
    if file.endswith(".csv"):   #Creates file exception for csv files within the cwd
        file_path = f"{cwd}\{file}" #Finds the csv files within the cwd
        shout(file_path)    #runs the function

# open the filehandle for reading the PSI input
#
        header ='PSI'
        with open(file_path) as psi_filehandle: #was PSI_OG0000004.txt
            for line in psi_filehandle.readlines():
                line = line.strip('\r\n')

        #
        # Skip the header
        #
                if(header in line):
                    continue

                (psi,species_a,species_b)=line.split(',')
        #
        # for some reason the CSV download uses double-quotes on every column
        # so here we remove them by replacing them with an empty string
        #
                psi = psi.replace('"','')
                species_a = species_a.replace('"','')
                species_b = species_b.replace('"','')

        #
        # when reading from file, the contents are strings
        # if you want to compare numbers, if you have to explicitly convert
        # the strings into numbers
        #
                psi=float(psi)
        #
                if (psi < .80): #Creates the 80% threshold for Taxol-predicted-genes in Orthofinder
                    continue
        # add a condition that filters psi for the minimum of 80%
        #

        #
        # The ordering of "Species A" and Species B" is random
        # So need to decide which one goes in which column
        #

                column_one = "" # This will be the UniProt ID
                column_two = "" # This will be the predicted gene ID

                if("Taxus_chinensis" in species_a):
                    column_one = species_b
                    column_two = species_a
                elif("Taxus_chinensis" in species_b):
                    column_one = species_a
                    column_two = species_b

        #
                (a, column_one, b) = column_one.split('|')
        # the identifier for column one should be just the UniProt ID
        # but the identifiers used in the file have other text, i.e. sp|Q84KI1|T14H_TAXCU
        # use the split function to extract the actual UniProt ID
        #

        #
        # write to the predicted-genes file
        #
                pg_filehandle.write('\t'.join([column_one,column_two,str(psi)])+'\n')



psi_filehandle.close()
pg_filehandle.close()
