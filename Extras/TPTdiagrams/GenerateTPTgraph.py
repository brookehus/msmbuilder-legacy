from msmbuilder import arglib
from msmbuilder import plot_graph
import numpy as np
from scipy import io, sparse
import sys
import glob

def run(Matrix, EqPops, ImageDir, Directed=False, EdgeScale=1, PopCutoff=0.01, EdgeCutoff=0.0, OutputFile='Graph.dot'):

    if ImageDir != 'none': pngs = glob.glob(ImageDir+'/*.png')
    else: pngs = None
    G = plot_graph.CreateNetwork(Matrix,EqPops,Directed=Directed,EdgeScale=EdgeScale,PopCutoff=PopCutoff,EdgeCutoff=EdgeCutoff,ImageList=pngs)

    plot_graph.PlotNetwork(G,OutputFile=OutputFile)

if __name__ == "__main__":
    parser = arglib.ArgumentParser(description="""
Draws a representation of your MSM and draws a graph corresponding to it. This graph
is written as a .dot file, which can be read by many common graph utilities. Read in MSM info
as a counts, transition, or net flux matrix.

Note: You need networkx and either Graphviz & PyGraphviz or pydot to get this utility working.
To get the graph the way you want it to look, you might want to open up this script and play
with some default parameters (EdgeScale=1, PopCutoff=0.01, EdgeCutoff=0.1) in the run() function.\n\n""")
    parser.add_argument('tmat', description='Name of the matric to represent as a graph. Can be counts, transition, or net flux matrix. Should be in .mtx format')
    parser.add_argument('populations', description='Populations file', default='Populations.dat')
    parser.add_argument('directed', description='Make the graph directed (if, e.g., a net flux matrix)', action='store_true', default=False)
    parser.add_argument('input', description="Directory containing node impages generated by 'RenderStateImages.py' that will be associated with the graph (optional)", default='none')
    parser.add_argument('output', description='Name of the dot file to write.', default='Graph.dot')
    parser.add_argument('epsilon', description='Cutoff for merging SL states.', default=0.1, type=float)
    args = parser.parse_args()
    print args

    matrix = io.mmread(args.tmat)
    populations = np.loadtxt(args.populations, dtype=float)
    
    run(matrix, populations, args.input, Directed=args.directed, OutputFile=args.output, PopCutoff=args.epsilon)
