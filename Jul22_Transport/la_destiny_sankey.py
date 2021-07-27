import plotly.graph_objects as go
import numpy as np
import sys

A = np.loadtxt(sys.argv[1]) #, dtype = np.int)
#print(A)

fig = go.Figure(data=[go.Sankey(
    node = dict(
      pad = 15,
      thickness = 20,
      line = dict(color = "black", width = 0.5),
      label = ["Born directly from hydro", "Born from 2->1 formation, such as e.g. pi pi->rho", "Born from some 2->n inelastic reaction", "Born from decay of high resonance originating from hydro", "Born from decay of higher resonance not originating from hydro",
               "Detectable: decayed and products not collided", "Formed higher resonance", "Reacted inelastically", "Undetectable: decay products collided"],
      color = ["blue", "red", "green", "black", "yellow", "brown", "orange", "aquamarine", "gray"]
    ),
    link = dict(
      source = [0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4],
      target = [5, 6, 7, 8, 5, 6, 7, 8, 5, 6, 7, 8, 5, 6, 7, 8, 5, 6, 7, 8],
      value = [A[0,0], A[0,1], A[0,2], A[0,3],
               A[1,0], A[1,1], A[1,2], A[1,3],
               A[2,0], A[2,1], A[2,2], A[2,3],
               A[3,0], A[3,1], A[3,2], A[3,3],
               A[4,0], A[4,1], A[4,2], A[4,3]]
  ))])

fig.update_layout(title_text="Destiny of rho0 in 0-10% central AuAu collisions at 200 GeV", font_size=20)
fig.show()
