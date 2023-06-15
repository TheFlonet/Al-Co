# MST efficient PLI version

Grafo non direzionato $G = (V, E)$, V sono i vertici di cardinalità n, E sono gli archi.

Grafo connesso = cammino per ogni coppia di vertici

Per la rappresentazione si usa la matrice di Laplace, G è definito come $L :== (l_{ij})_{n\times n}$ tale che L = D - A, dove D è il grado della matrice e A è la matrice di adiacenza

$$l_{ij} = \begin{cases}
        deg(v_i) & i = j\\
        -1 & i \neq j \land v_i \text{ è adiacente a } v_j \\
        0 & \text{altrimenti}
    \end{cases}$$

La matrice dei pesi $W = (w_{ij})_{n\times n}$ con tutti i pesi positivi per ogni arco in E

Kruskal trova sia Minimum spanning tree che minimum spanning forest ($O(|E|log|V|)$)

$x_ij \in {0, 1}$ indica che $(i, j) \in E$ se $x_{ij} = 1$

Il vettore $x^*$ indica con 1 tutti gli archi presi, con 0 quelli non presi (ordinando gli archi in qualsivoglia modo è sempre possibile effettuare questo passaggio)

## Formulazioni con un numero polinomiale di vincoli

Un numero polinomiale di vincoli permette di creare poliedri con un numero polinomiale di vertici, quindi utilizzando algoritmi come quello del simplesso si possono risolvere in modo efficiente

<!-- ### Single-commodity flow formulation

$$\min_{x, f} \sum_{(i, j) \in E}w_{ij}x_{ij}$$

$$s.t.
\begin{cases}
    \sum_{(i, j) \in E}x_{ij} = n-1 \\
    \sum_jf_{j1} - \sum_jf_{1j} = n-1 \\
    \sum_jf_{ji} - \sum_jf_{ij} = 1, \forall i \in V, i \neq 1 \\
    f_{ij} \leq (n-1)x_{ij}, f_{ji} \leq (n-1)=x_{ij}, \forall (i, j) \in E \\
    f_{ij} \geq 0, \forall (i, j) \in E \cup E' \\
    x_{ij} \in \{0, 1\}, \forall (i, j) \in E
\end{cases}
$$

Dove $f_{ij}$ indica il flusso da $v_i$ a $v_j$, $E'$ indica gli archi di direzione opposta rispetto ad $E$ -->

### Martin's formulation

Martin: Using separation algorithms to generate mixed integer model reformulations. (Operations Research Letters 10, 119-128, 1991)

$$\min_{x, f} \sum_{(i, j) \in E}w_{ij}x_{ij}$$

$$s.t.
\begin{cases}
    \sum_{(i, j) \in E}x_{ij} = n-1 \\
    y_{ij}^k + y_{ji}^k = x_{ij}, \forall (i, j) \in E, k \in V \\
    \sum_{k \in V\setminus\{i,j\}}y_{ik}^j + x_{ij} = 1, \forall (i, j) \in E \\
    x_{ij}, y_{ij}^k, y_{ji}^k \in \{0, 1\}, \forall (i, j) \in E, k \in V
\end{cases}
$$

Dove $y_{ij}^k$ indica che l'arco $(i, j)$ è nello spanning tree e il vertice k è nel lato di j (togliendo l'arco j e k rimarrebbero connessi) se $y_{ij}^k$ è 1, se è posta a 0 indica che l'arco è nell'albero ma k non si trova dallo stesso lato di j

Il primo vincolo assicura che il sottografo abbia il numero di archi che caratterizzano un albero

Il secondo vincolo garantisce che se l'arco $(i, j)$ è messo nell'albero ($x_{ij} = 1$), ogni vertice k deve appartenenere al lato di y o al lato di i, se l'arco non è selezionato ($x_{ij} = 0$) i vertici possono essere nel lato di i, nel lato di j o in nessuno dei due lati

Il terzo vincolo assicura che se l'arco è nell'albero ($x_{ij} = 1$), gli archi $(i, k)$ che connettono i sono nel lato di i ($y_{ik}^j = y_{ij}^k = 0, y_{ij}^k = 1$). Se l'arco non è inserito ($x_{ij} = 0$) deve esistere un arco $(i, k)$ tale che j è nel lato di k ($y_{ik}^j = 1$ per qualche k)
