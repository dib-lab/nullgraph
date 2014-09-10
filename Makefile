KHMER=/u/t/dev/khmer

all: genome.fa reads-nobias.fa reads-bias-nonrandom.fa reads-bias-nonrandom.fa \
	metag-reads.fa reads-bias-nonrandom.dens  reads-bias-random.dens  reads-nobias.dens reads-bias-random.r1.dens reads-bias-random.r3.dens reads-bias-random.r5.dens repreads-bias-random.dens ecoli-bias-random.dens ecoli-nobias.dens  reads-nobias.posdens65 \
	reads-nobias.posdens10 \
	reads-bias-random.posdens65 \
	reads-bias-random.posdens10 \
	reads-bias-nonrandom.posdens65 \
	reads-bias-nonrandom.posdens10 \
	repreads-bias-random.posdens65 \
	repreads-bias-random.posdens10 \
	corn-50m-lump.posdens40 \
	corn-50m-lump.posdens10 \
	corn-50m-lump.dens

genome.fa:
	python make-random-genome.py > genome.fa

repgenome.fa:
	python make-random-genome-with-repeats.py > repgenome.fa

reads-nobias.fa: genome.fa
	python make-reads.py genome.fa > reads-nobias.fa

reads-bias-random.fa: genome.fa
	python make-reads-biased-random.py genome.fa > reads-bias-random.fa

repreads-bias-random.fa: repgenome.fa
	python make-reads-biased-random.py repgenome.fa > repreads-bias-random.fa

reads-bias-nonrandom.fa: genome.fa
	python make-reads-biased-nonrandom.py genome.fa > reads-bias-nonrandom.fa

ecoli-nobias.fa.gz: ecoliMG1655.fa
	python make-reads.py ecoliMG1655.fa | gzip -9c > ecoli-nobias.fa.gz

ecoli-bias-random.fa.gz: ecoliMG1655.fa
	python make-reads-biased-random.py ecoliMG1655.fa | gzip -9c > ecoli-bias-random.fa.gz

transcripts.fa:
	python make-random-transcriptome.py > transcripts.fa

metag-reads.fa: transcripts.fa
	python make-biased-reads.py transcripts.fa > metag-reads.fa

reads-nobias.ht: reads-nobias.fa
	python $(KHMER)/scripts/load-graph.py -k 32 -N 4 -x 1e9 --no-build-tagset reads-nobias reads-nobias.fa

reads-nobias.dens: reads-nobias.ht
	python $(KHMER)/sandbox/count-density-by-position.py -n 10000 reads-nobias.ht reads-nobias.fa reads-nobias.dens

reads-nobias.posdens65: reads-nobias.ht
	python $(KHMER)/sandbox/count-density-at-position.py -P 65 -n 100000 reads-nobias.ht reads-nobias.fa reads-nobias.posdens65

reads-nobias.posdens10: reads-nobias.ht
	python $(KHMER)/sandbox/count-density-at-position.py -P 10 -n 100000 reads-nobias.ht reads-nobias.fa reads-nobias.posdens10

reads-bias-random.ht: reads-bias-random.fa
	python $(KHMER)/scripts/load-graph.py -k 32 -N 4 -x 1e9 --no-build-tagset reads-bias-random reads-bias-random.fa

reads-bias-random.dens: reads-bias-random.ht
	python $(KHMER)/sandbox/count-density-by-position.py -n 10000 reads-bias-random.ht reads-bias-random.fa reads-bias-random.dens

reads-bias-random.posdens65: reads-bias-random.ht
	python $(KHMER)/sandbox/count-density-at-position.py -P 65 -n 100000 reads-bias-random.ht reads-bias-random.fa reads-bias-random.posdens65

reads-bias-random.posdens10: reads-bias-random.ht
	python $(KHMER)/sandbox/count-density-at-position.py -P 10 -n 100000 reads-bias-random.ht reads-bias-random.fa reads-bias-random.posdens10

reads-bias-random.r1.dens: reads-bias-random.ht
	python $(KHMER)/sandbox/count-density-by-position.py -r 1 -n 10000 reads-bias-random.ht reads-bias-random.fa reads-bias-random.r1.dens

reads-bias-random.r3.dens: reads-bias-random.ht
	python $(KHMER)/sandbox/count-density-by-position.py -r 3 -n 10000 reads-bias-random.ht reads-bias-random.fa reads-bias-random.r3.dens

reads-bias-random.r5.dens: reads-bias-random.ht
	python $(KHMER)/sandbox/count-density-by-position.py -r 5 -n 10000 reads-bias-random.ht reads-bias-random.fa reads-bias-random.r5.dens

reads-bias-nonrandom.ht: reads-bias-nonrandom.fa
	python $(KHMER)/scripts/load-graph.py -k 32 -N 4 -x 1e9 --no-build-tagset reads-bias-nonrandom reads-bias-nonrandom.fa

reads-bias-nonrandom.dens: reads-bias-nonrandom.ht
	python $(KHMER)/sandbox/count-density-by-position.py -n 10000 reads-bias-nonrandom.ht reads-bias-nonrandom.fa reads-bias-nonrandom.dens

reads-bias-nonrandom.posdens65: reads-bias-nonrandom.ht
	python $(KHMER)/sandbox/count-density-at-position.py -P 65 -n 100000 reads-bias-nonrandom.ht reads-bias-nonrandom.fa reads-bias-nonrandom.posdens65

reads-bias-nonrandom.posdens10: reads-bias-nonrandom.ht
	python $(KHMER)/sandbox/count-density-at-position.py -P 10 -n 100000 reads-bias-nonrandom.ht reads-bias-nonrandom.fa reads-bias-nonrandom.posdens10

repreads-bias-nonrandom.posdens65: repreads-bias-nonrandom.ht
	python $(KHMER)/sandbox/count-density-at-position.py -P 65 -n 100000 repreads-bias-nonrandom.ht repreads-bias-nonrandom.fa repreads-bias-nonrandom.posdens65

repreads-bias-nonrandom.posdens10: repreads-bias-nonrandom.ht
	python $(KHMER)/sandbox/count-density-at-position.py -P 10 -n 100000 repreads-bias-nonrandom.ht repreads-bias-nonrandom.fa repreads-bias-nonrandom.posdens10

repreads-bias-random.ht: repreads-bias-random.fa
	python $(KHMER)/scripts/load-graph.py -k 32 -N 4 -x 1e9 --no-build-tagset repreads-bias-random repreads-bias-random.fa

repreads-bias-random.dens: repreads-bias-random.ht
	python $(KHMER)/sandbox/count-density-by-position.py -n 10000 repreads-bias-random.ht repreads-bias-random.fa repreads-bias-random.dens

repreads-bias-random.posdens65: repreads-bias-random.ht
	python $(KHMER)/sandbox/count-density-at-position.py -P 65 -n 100000 repreads-bias-random.ht repreads-bias-random.fa repreads-bias-random.posdens65

repreads-bias-random.posdens10: repreads-bias-random.ht
	python $(KHMER)/sandbox/count-density-at-position.py -P 10 -n 100000 repreads-bias-random.ht repreads-bias-random.fa repreads-bias-random.posdens10

ecoli-nobias.ht: ecoli-nobias.fa.gz
	python $(KHMER)/scripts/load-graph.py -k 32 -N 4 -x 1e9 --no-build-tagset ecoli-nobias ecoli-nobias.fa.gz

ecoli-nobias.dens: ecoli-nobias.ht
	python $(KHMER)/sandbox/count-density-by-position.py -n 10000 ecoli-nobias.ht ecoli-nobias.fa.gz ecoli-nobias.dens

ecoli-bias-random.ht: ecoli-bias-random.fa.gz
	python $(KHMER)/scripts/load-graph.py -k 32 -N 4 -x 1e9 --no-build-tagset ecoli-bias-random ecoli-bias-random.fa.gz

ecoli-bias-random.dens: ecoli-bias-random.ht
	python $(KHMER)/sandbox/count-density-by-position.py -n 10000 ecoli-bias-random.ht ecoli-bias-random.fa.gz ecoli-bias-random.dens

corn-50m-lump.ht: corn-50m-lump.fa.gz
	python $(KHMER)/scripts/load-graph.py -k 32 -N 4 -x 4e9 --no-build-tagset corn-50m-lump corn-50m-lump.fa.gz

corn-50m-lump.dens: corn-50m-lump.ht
	python $(KHMER)/sandbox/count-density-by-position.py -n 10000 corn-50m-lump.ht corn-50m-lump.fa.gz corn-50m-lump.dens

corn-50m-lump.posdens40: corn-50m-lump.ht
	python $(KHMER)/sandbox/count-density-at-position.py -P 40 -n 100000 corn-50m-lump.ht corn-50m-lump.fa.gz corn-50m-lump.posdens40

corn-50m-lump.posdens10: corn-50m-lump.ht
	python $(KHMER)/sandbox/count-density-at-position.py -P 10 -n 100000 corn-50m-lump.ht corn-50m-lump.fa.gz corn-50m-lump.posdens10
