def list_to_fasta(seqs, headers, output_file):
  """ write sequences in the list `seqs' in fasta format to file
      `output_file'.
  """
  fout = open(output_file, 'w+')
  out = '\n'.join(['>' + headers[i] + "\n" + j for i,j in enumerate(seqs)])
  fout.write(out)
  fout.close()
  
def fasta_to_list(fileName, returnHeader = False):
  inFile = open(fileName,'r')

  headerList = []
  seqList = []
  currentSeq = ''
  for line in inFile:
    if line[0] == ">":
      headerList.append(line[1:].strip())
      if currentSeq != '':
        seqList.append(currentSeq)

      currentSeq = ''
    else:
      currentSeq += line.strip()
  inFile.close()
  seqList.append(currentSeq)
  
  if returnHeader:
    return seqList, headerList
  return seqList