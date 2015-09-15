import sys
import scipy
import numpy
import math
import scipy.linalg as la

# global memoization table for volintegral
_memo_vol_max = 11
_memo_volintegral = [[[None for i in range(_memo_vol_max)] for j in range(_memo_vol_max)] for k in range(_memo_vol_max)]
# global memoization table for double factorial
_memo_max = 1024
_memo_doublefact = [None for i in range(_memo_max)]
_memo_doublefact[0] = 1
_memo_doublefact[1] = 1

def compute_dyda(ns,hextype,r,tabs,d1,d2,d3,shape,ifw,ndata,z,wsort,indice):
    dyda = numpy.zeros((ns,ndata))

    # isotropic case
    if ns == 2:
        dc_c11 = dstiff_iso_c11()
        dc_c44 = dstiff_iso_c44()
        
        dgamma_c11 = dgamma_fill(tabs,r,d1,d2,d3,dc_c11,shape)
        dgamma_c44 = dgamma_fill(tabs,r,d1,d2,d3,dc_c44,shape)

        # gradiant of the objective function
        iw = ifw
        for i in range(ndata):
            dyda[0][i] = dfdp(wsort[iw], dgamma_c11, z, indice[iw], r)
            dyda[1][i] = dfdp(wsort[iw], dgamma_c44, z, indice[iw], r)
            iw += 1

    # cubic
    elif ns == 3:
        dc_c11 = dstiff_cub_c11()
        dc_c12 = dstiff_cub_c12()
        dc_c44 = dstiff_cub_c44()
    
        dgamma_c11 = dgamma_fill(tabs,r,d1,d2,d3,dc_c11,shape)
        dgamma_c12 = dgamma_fill(tabs,r,d1,d2,d3,dc_c12,shape)
        dgamma_c44 = dgamma_fill(tabs,r,d1,d2,d3,dc_c44,shape)

        # gradiant of the objective function
        iw = ifw
        for i in range(ndata):
            dyda[0][i]=dfdp(wsort[iw], dgamma_c11, z, indice[iw], r)
            dyda[1][i]=dfdp(wsort[iw], dgamma_c12, z, indice[iw], r)
            dyda[2][i]=dfdp(wsort[iw], dgamma_c44, z, indice[iw], r)
            iw += 1

    # hexagonal - VTI
    elif ns == 5 and hextype == 1:
        dc_c33 = dstiff_vti_c33()
        dc_c23 = dstiff_vti_c23()
        dc_c12 = dstiff_vti_c12()
        dc_c44 = dstiff_vti_c44()
        dc_c66 = dstiff_vti_c66()
    
        dgamma_c33 = dgamma_fill(tabs, r, d1, d2, d3, dc_c33, shape)
        dgamma_c23 = dgamma_fill(tabs, r, d1, d2, d3, dc_c23, shape)
        dgamma_c12 = dgamma_fill(tabs, r, d1, d2, d3, dc_c12, shape)
        dgamma_c44 = dgamma_fill(tabs, r, d1, d2, d3, dc_c44, shape)
        dgamma_c66 = dgamma_fill(tabs, r, d1, d2, d3, dc_c66, shape)
    
        # gradiant of the objective function
        iw = ifw
        for i in range(ndata):
            dyda[0][i]=dfdp(wsort[iw], dgamma_c33, z, indice[iw], r)
            dyda[1][i]=dfdp(wsort[iw], dgamma_c23, z, indice[iw], r)
            dyda[2][i]=dfdp(wsort[iw], dgamma_c12, z, indice[iw], r)
            dyda[3][i]=dfdp(wsort[iw], dgamma_c44, z, indice[iw], r)
            dyda[4][i]=dfdp(wsort[iw], dgamma_c66, z, indice[iw], r)
            iw += 1
   
    elif ns == 5 and hextype == 2:
        dc_c11 = dstiff_hti_c11()
        dc_c33 = dstiff_hti_c33()
        dc_c12 = dstiff_hti_c12()
        dc_c44 = dstiff_hti_c44()
        dc_c66 = dstiff_hti_c66()

        dgamma_c11 = dgamma_fill(tabs, r, d1, d2, d3, dc_c33, shape)
        dgamma_c33 = dgamma_fill(tabs, r, d1, d2, d3, dc_c33, shape)
        dgamma_c12 = dgamma_fill(tabs, r, d1, d2, d3, dc_c12, shape)
        dgamma_c44 = dgamma_fill(tabs, r, d1, d2, d3, dc_c44, shape)
        dgamma_c66 = dgamma_fill(tabs, r, d1, d2, d3, dc_c66, shape)

        # gradiant of the objective function
        iw = ifw
        for i in range(ndata):
            dyda[0][i]=dfdp(wsort[iw], dgamma_c11, z, indice[iw], r)
            dyda[1][i]=dfdp(wsort[iw], dgamma_c33, z, indice[iw], r)
            dyda[2][i]=dfdp(wsort[iw], dgamma_c12, z, indice[iw], r)
            dyda[3][i]=dfdp(wsort[iw], dgamma_c44, z, indice[iw], r)
            dyda[4][i]=dfdp(wsort[iw], dgamma_c66, z, indice[iw], r)
            iw += 1

    # tetragonal
    elif ns == 6:
        dc_c11 = dstiff_tetra_c11()
        dc_c33 = dstiff_tetra_c33()
        dc_c23 = dstiff_tetra_c23()
        dc_c12 = dstiff_tetra_c12()
        dc_c44 = dstiff_tetra_c44()
        dc_c66 = dstiff_tetra_c66()

        dgamma_c11 = dgamma_fill(tabs, r, d1, d2, d3, dc_c11, shape)
        dgamma_c33 = dgamma_fill(tabs, r, d1, d2, d3, dc_c33, shape)
        dgamma_c23 = dgamma_fill(tabs, r, d1, d2, d3, dc_c23, shape)
        dgamma_c12 = dgamma_fill(tabs, r, d1, d2, d3, dc_c12, shape)
        dgamma_c44 = dgamma_fill(tabs, r, d1, d2, d3, dc_c44, shape)
        dgamma_c66 = dgamma_fill(tabs, r, d1, d2, d3, dc_c66, shape)
    
        # gradiant of the objective function
        iw = ifw
        for i in range(ndata):
            dyda[0][i]=dfdp(wsort[iw], dgamma_c11, z, indice[iw], r)
            dyda[1][i]=dfdp(wsort[iw], dgamma_c33, z, indice[iw], r)
            dyda[2][i]=dfdp(wsort[iw], dgamma_c23, z, indice[iw], r)
            dyda[3][i]=dfdp(wsort[iw], dgamma_c12, z, indice[iw], r)
            dyda[4][i]=dfdp(wsort[iw], dgamma_c44, z, indice[iw], r)
            dyda[5][i]=dfdp(wsort[iw], dgamma_c66, z, indice[iw], r)
            iw += 1

    # orthorhombic
    elif ns == 9:
        dc_c11 = dstiff_orth_c11()
        dc_c22 = dstiff_orth_c22()
        dc_c33 = dstiff_orth_c33()
        dc_c23 = dstiff_orth_c23()
        dc_c13 = dstiff_orth_c13()
        dc_c12 = dstiff_orth_c12()
        dc_c44 = dstiff_orth_c44()
        dc_c55 = dstiff_orth_c55()
        dc_c66 = dstiff_orth_c66()
    
        dgamma_c11=dgamma_fill(tabs, r, d1, d2, d3, dc_c11, shape)
        dgamma_c22=dgamma_fill(tabs, r, d1, d2, d3, dc_c22, shape)
        dgamma_c33=dgamma_fill(tabs, r, d1, d2, d3, dc_c33, shape)
        dgamma_c23=dgamma_fill(tabs, r, d1, d2, d3, dc_c23, shape)
        dgamma_c13=dgamma_fill(tabs, r, d1, d2, d3, dc_c13, shape)
        dgamma_c12=dgamma_fill(tabs, r, d1, d2, d3, dc_c12, shape)
        dgamma_c44=dgamma_fill(tabs, r, d1, d2, d3, dc_c44, shape)
        dgamma_c55=dgamma_fill(tabs, r, d1, d2, d3, dc_c55, shape)
        dgamma_c66=dgamma_fill(tabs, r, d1, d2, d3, dc_c66, shape)
    
        # gradiant of the objective function
        iw = ifw
        for i in range(ndata):
            dyda[0][i]=dfdp(wsort[iw], dgamma_c11, z, indice[iw], r)
            dyda[1][i]=dfdp(wsort[iw], dgamma_c22, z, indice[iw], r)
            dyda[2][i]=dfdp(wsort[iw], dgamma_c33, z, indice[iw], r)
            dyda[3][i]=dfdp(wsort[iw], dgamma_c23, z, indice[iw], r)
            dyda[4][i]=dfdp(wsort[iw], dgamma_c13, z, indice[iw], r)
            dyda[5][i]=dfdp(wsort[iw], dgamma_c12, z, indice[iw], r)
            dyda[6][i]=dfdp(wsort[iw], dgamma_c44, z, indice[iw], r)
            dyda[7][i]=dfdp(wsort[iw], dgamma_c55, z, indice[iw], r)
            dyda[8][i]=dfdp(wsort[iw], dgamma_c66, z, indice[iw], r)
            iw += 1

    return dyda



# isotropic
def dstiff_iso_c11():
    cm = numpy.zeros((6,6))
    cm[0][0] = 10.0
    cm[1][1] = cm[2][2] = cm[0][0]
    cm[0][1] = cm[0][2] = cm[1][2] = cm[0][0]
    cm[1][0] = cm[2][0] = cm[2][1] = cm[0][0]
    return stiffness(cm)

def dstiff_iso_c44():
    cm = numpy.zeros((6,6))
    cm[3][3] = 1.0
    cm[4][4] = cm[5][5] = cm[3][3]
    cm[0][1] = cm[0][2] = cm[1][2] = -2.0 * cm[3][3]
    cm[1][0] = cm[2][0] = cm[2][1] = -2.0 * cm[3][3]
    return stiffness(cm)

# cubic
def dstiff_cub_c11():
    cm = numpy.zeros((6,6))
    cm[0][0] = 10.0
    cm[1][1] = cm[2][2] = cm[0][0]
    return stiffness(cm)

def dstiff_cub_c12():
    cm = numpy.zeros((6,6))
    cm[0][1] = 10.0
    cm[0][2] = cm[1][2] = cm[0][1]
    cm[2][0] = cm[2][1] = cm[1][0] = cm[0][1]
    return stiffness(cm)

def dstiff_cub_c44():
    cm = numpy.zeros((6,6))
    cm[3][3] = 1.0
    cm[4][4] = cm[5][5] = cm[3][3]
    return stiffness(cm)

# VTI
def dstiff_vti_c33():
    cm = numpy.zeros((6,6))
    cm[2][2] = 10.0
    return stiffness(cm)

def dstiff_vti_c23():
    cm = numpy.zeros((6,6))
    cm[1][2] = 10.0
    cm[0][2] = cm[2][0] = cm[2][1] = cm[1][2]
    return stiffness(cm)

def dstiff_vti_c12():
    cm = numpy.zeros((6,6))
    cm[0][1] = 10.0
    cm[0][0] = cm[1][1] = cm[0][1]
    cm[1][0] = cm[0][1]
    return stiffness(cm)

def dstiff_vti_c44():
    cm = numpy.zeros((6,6))
    cm[3][3] = 1.0
    cm[4][4] = cm[3][3]
    return stiffness(cm)

def dstiff_vti_c66():
    cm = numpy.zeros((6,6))
    cm[5][5] = 1.0
    cm[0][0] = cm[1][1] = 2.0 * cm[5][5]
    return stiffness(cm)

# HTI
def dstiff_hti_c11():
    cm = numpy.zeros((6,6))
    cm[0][0] = 10.0
    return stiffness(cm)

def dstiff_hti_c33():
    cm = numpy.zeros((6,6))
    cm[2][2] = 10.0
    cm[1][1] = cm[2][2]
    return stiffness(cm)

def dstiff_hti_c12():
    cm = numpy.zeros((6,6))
    cm[0][1] = 10.0
    cm[0][2] = cm[1][0] = cm[2][0] = cm[0][1]
    return stiffness(cm)

def dstiff_hti_c44():
    cm = numpy.zeros((6,6))
    cm[3][3] = 1.0
    return stiffness(cm)

def dstiff_hti_c66():
    cm = numpy.zeros((6,6))
    cm[5][5] = 1.0
    cm[4][4] = cm[5][5]
    return stiffness(cm)

# Tetragonal
def dstiff_tetra_c11():
    cm = numpy.zeros((6,6))
    cm[1][1] = cm[0][0] = 10.0
    return stiffness(cm)

def dstiff_tetra_c33():
    cm = numpy.zeros((6,6))
    cm[2][2] = 10.0
    return stiffness(cm)

def dstiff_tetra_c23():
    cm = numpy.zeros((6,6))
    cm[1][2] = 10.0
    cm[0][2] = cm[2][0] = cm[2][1] = cm[1][2]
    return stiffness(cm)

def dstiff_tetra_c12():
    cm = numpy.zeros((6,6))
    cm[0][1] = 10.0
    cm[1][0] = cm[0][1]
    return stiffness(cm)

def dstiff_tetra_c44():
    cm = numpy.zeros((6,6))
    cm[3][3] = 1.0
    cm[4][4] = cm[3][3]
    return stiffness(cm)

def dstiff_tetra_c66():
    cm = numpy.zeros((6,6))
    cm[5][5] = 1.0
    return stiffness(cm)

# Orthorhombic
def dstiff_orth_c11():
    cm = numpy.zeros((6,6))
    cm[0][0] = 10.0
    return stiffness(cm)

def dstiff_orth_c22():
    cm = numpy.zeros((6,6))
    cm[1][1] = 10.0
    return stiffness(cm)

def dstiff_orth_c33(): 
    cm = numpy.zeros((6,6))
    cm[2][2] = 10.0
    return stiffness(cm)

def dstiff_orth_c23():
    cm = numpy.zeros((6,6))
    cm[1][2] = 10.0
    cm[2][1] = cm[1][2]
    return stiffness(cm)

def dstiff_orth_c13():
    cm = numpy.zeros((6,6))
    cm[0][2] = 10.0
    cm[2][0] = cm[0][2]
    return stiffness(cm)

def dstiff_orth_c12():
    cm = numpy.zeros((6,6))
    cm[0][1] = 10.0
    cm[1][0] = cm[0][1]
    return stiffness(cm)

def dstiff_orth_c44():
    cm = numpy.zeros((6,6))
    cm[3][3] = 1.0
    return stiffness(cm)

def dstiff_orth_c55():
    cm = numpy.zeros((6,6))
    cm[4][4] = 1.0
    return stiffness(cm)

def dstiff_orth_c66():
    cm = numpy.zeros((6,6))
    cm[5][5] = 1.0
    return stiffness(cm)



def dgamma_fill(tabs,r,d1,d2,d3,dc,shape):
    dgamma = numpy.zeros((r,r))
    for ir1 in range(r):
        tabs1 = tabs[ir1]
        for ir2 in range(r):
            tabs2 = tabs[ir2]
            gamma_helper(dgamma,dc,tabs1,tabs2,ir1,ir2,d1,d2,d3,shape)
    return dgamma



def gamma_helper(gamma,c,tabs1,tabs2,ir1,ir2,d1,d2,d3,shape):
    [i1,l1,m1,n1] = tabs1
    [i2,l2,m2,n2] = tabs2
    l = l1 + l2
    m = m1 + m2
    n = n1 + n2
    if l1 > 0:
        [st1,st2,st3] = c[i1][0][i2]
        if l % 2 == 0:
            if st1 != 0 and l2 > 0 and m % 2 == 0 and n % 2 == 0:
                gamma[ir1][ir2] += st1 * l1 * l2 * volintegral(d1, d2, d3, l-2, m, n, shape)
        elif m % 2 == 1:
            if st2 != 0 and m2 > 0 and n % 2 == 0:
                gamma[ir1][ir2] += st2 * l1 * m2 * volintegral(d1, d2, d3, l-1, m-1, n, shape)
        elif n % 2 == 1:
            if st3 != 0 and n2 > 0:
                gamma[ir1][ir2] += st3 * l1 * n2 * volintegral(d1, d2, d3, l-1, m, n-1, shape)
    if m1 > 0:
        [st1,st2,st3] = c[i1][1][i2]
        if l % 2 == 1:
            if st1 != 0 and l2 > 0 and m % 2 == 1 and n % 2 == 0:
                gamma[ir1][ir2] += st1 * m1 * l2 * volintegral(d1, d2, d3, l-1, m-1, n, shape)
        elif m % 2 == 0:
            if st2 != 0 and m2 > 0 and n % 2 == 0:
                gamma[ir1][ir2] += st2 * m1 * m2 * volintegral(d1, d2, d3, l, m-2, n, shape)
        elif n % 2 == 1:
            if st3 != 0 and n2 > 0:
                gamma[ir1][ir2] += st3 * m1 * n2 * volintegral(d1, d2, d3, l, m-1, n-1, shape)
    if n1 > 0:
        [st1,st2,st3] = c[i1][2][i2]
        if l % 2 == 1:
            if st1 != 0 and l2 > 0 and m % 2 == 0 and n % 2 == 1:
                gamma[ir1][ir2] += st1 * n1 * l2 * volintegral(d1, d2, d3, l-1, m, n-1, shape)
        elif m % 2 == 1:
            if st2 != 0 and m2 > 0 and n % 2 == 1:
                gamma[ir1][ir2] += st2 * n1 * m2 * volintegral(d1, d2, d3, l, m-1, n-1, shape)
        elif n % 2 == 0:
            if st3 != 0 and n2 > 0:
                gamma[ir1][ir2] += st3 * n1 * n2 * volintegral(d1, d2, d3, l, m, n-2, shape)



def dfdp(f, dgammadp, z, ie, n):
    p = []
    for i in range(n):
        # we use dgammadp's 
        # symmetry here
        p.append(numpy.dot(dgammadp[i],z[ie])) 
    return numpy.dot(z[ie],p) / (8.0 * scipy.pi * scipy.pi * f)



#/* ----------------------------------------------------------- */
#/* ----------------------------------------------------------- */
#/* ----------------  Optimization routines  ------------------ */
#/* ----------------------------------------------------------- */
#/* ----------------------------------------------------------- */


# -------------------------------------------------------------------
# ---------------------------- COVSRT -------------------------------
# -------------------------------------------------------------------
# ------------------------- Description from: -----------------------
# -------- Numerical Recipes: the art of scientific computing -------
# --W. H. Press, B. P. Flannery, S. A. Teukolsky, W. T, Vetterling --
# -------------------------------------------------------------------

# subroutine COVSRT(COVAR, NCVM, MA, LISTA, MFIT)
# Given the covariance matrix COVAR of a fir for MFIT of MA total 
# parameters, and their ordering LISTA(I), repack the covariance matrix 
# to the true order of the parameters. Elements associated with fixed
# parameters will be zero. NCVM is the physical dimension of COVAR

def covsrt(covar, ma, ia, mfit):
    for i in range(mfit, ma):
        for j in range(i):
            covar[i][j] = covar[j][i] = 0.0
    k = mfit - 1
    for j in range(ma-1, -1, -1):
        if ia[j]:
            for i in range(ma):
                covar[i][k], covar[i][j] = covar[i][j], covar[i][k]
            for i in range(ma):
                covar[k][i], covar[j][i] = covar[j][i], covar[k][i]
        k -= 1



#/* ------------------------------------------------------------------- */
#/* ---------------------------- GAUSSJ ------------------------------- */
#/* ------------------------------------------------------------------- */
#/* ------------------------- Description from: ----------------------- */
#/* -------- Numerical Recipes: the art of scientific computing ------- */
#/* --W. H. Press, B. P. Flannery, S. A. Teukolsky, W. T, Vetterling -- */
#/* ------------------------------------------------------------------- */

#/* Subroutine GAUSSJ(A, N, NP, B, M, MP)
# * Linear equation solution by Gauss-Jordan elimination, equation (2.1.1)
# * above. A is an input matrix of N by N elements, stored in an array of
# * physical dimensions NP by NP. B is an input matrix of N by N containing
# * the M right-hand side vectors, stored in an array of physical 
# * dimensions Np by MP. On output, A is replaced by its matrix inverse,
# * and B is replaced by the corresponding set of solution vectors. */
def gaussj(a, n, b, m):
    indxc = []
    indxr = []
    ipiv  = [0 for j in range(n)]
    for i in range(n):
        big = 0.0
        for j in range(n):
            if ipiv[j] != 1:
                for k in range(n):
                    if ipiv[k] == 0:
                        if math.fabs(a[j][k]) >= big:
                            big = math.fabs(a[j][k])
                            irow = j
                            icol = k
                    elif ipiv[k] > 1:
                        raise RuntimeError('GAUSSJ: Singular Matrix-1')
        ++(ipiv[icol])
        if irow != icol:
            for l in range(n):
                a[irow][l], a[icol][l] = a[icol][l], a[irow][l]
            for l in range(m):
                b[l][irow], b[l][icol] = b[l][icol], b[l][irow]
        indxr.append(irow)
        indxc.append(icol)
        if a[icol][icol] == 0.0:
            raise RuntimeError('GAUSSJ: Singular Matrix-2')
        pivinv = 1.0 / a[icol][icol]
        a[icol][icol] = 1.0
        for l in range(n):
            a[icol][l] *= pivinv
        for l in range(m):
            b[icol][l] *= pivinv
        for ll in range(n):
            if ll != icol:
                dum = a[ll][icol]
                a[ll][icol] = 0.0
                for l in range(n):
                    a[ll][l] -= a[icol][l] * dum
                for l in range(m):
                    b[ll][l] -= b[icol][l] * dum
    for l in range(n-1,-1,-1):
        if indxr[l] != indxc[l]:
            for k in range(n):
                a[k][indxr[l]], a[k][indxc[l]] = a[k][indxc[l]], a[k][indxr[l]]

# -------------------------------------------------------------------
# ---------------------------- MRQCOF -------------------------------
# -------------------------------------------------------------------
# ------------------------- Description from: -----------------------
# -------- Numerical Recipes: the art of scientific computing -------
# --W. H. Press, B. P. Flannery, S. A. Teukolsky, W. T, Vetterling --
# -------------------------------------------------------------------

# Subroutine MRQCOF(X, Y, SIG, NDATA, A, MA, LISTA, MFIT, ALPHA, BETA,
# NALP, CHISQ, FUNCS)
# Used by MRQMIN to evaluate the linearized fitting matrix ALPHA, and 
# vector BETA from (14.4.8) 

# called by mrqmin_function each iteration. Computes "chisq"
def mrqcof(d,r,tabs,irk,d1,d2,d3,rho,shape,freqmin,y,sig,ndata,a,ia,ma,alpha,beta,hextype):

    mfit = 0
    for j in range(ma):
        if ia[j] != 0:
            mfit += 1
    for j in range(mfit):
        for k in range(j):
            alpha[j][k] = 0.0
        beta[j] = 0.0

    chisq = 0.0
    ymod, dyda = formod(d,r,tabs,irk,d1,d2,d3,rho,shape,freqmin,ndata,a,ma,hextype)
    for i in range(ndata):
        sig2i = sig[i] * sig[i]
        dy = y[i] - ymod[i]
        j = -1
        for l in range(ma):
            if ia[l] != 0:
                wt = dyda[l][i] * sig2i
                j += 1
                k = -1
                for m in range(l):
                    if ia[m] != 0:
                        k += 1
                        alpha[j][k] += wt * dyda[m][i]
                beta[j] += dy * wt
 
        chisq += dy * dy * sig2i
  
    # chisq prints from here
    print('chisq={0:.6f}\n'.format(100.0 * chisq))
    for j in range(1,mfit):
        for k in range(j-1):
            alpha[k][j] = alpha[j][k]

    return chisq


def formod(d,r,tabs,irk,d1,d2,d3,rho,shape,freqmin,ndata,a,ns,hextype):

    freqs = 'predictedf' # CHANGE THIS LINE TO APPROPRIATE DIRECTORY

    cm = make_cm(a,hextype)
    e = e_fill(tabs, r, d1, d2, d3, rho, shape, irk)
    gamma = gamma_fill(tabs, r, d1, d2, d3, cm, shape, irk)
      
  
    print('starting eigenvalues calculation')
    #/*-------------------------------------------------------------*/
    #/*--------- solve the generalized eigenvalue problem ----------*/
    #/*-------------------------------------------------------------*/  
    eigvals = []
    eigvect = []
    for k in range(8):
        # lapack routine
        w, v = la.eigh(gamma[k], e[k], lower=False, eigvals_only=False, turbo=False, type=1, overwrite_a=True, overwrite_b=True, check_finite=False)
        eigvals.append(w)
        eigvect.append(numpy.transpose(v))

    #/*-------------------------------------------------------------*/  
    #/*-------------------------------------------------------------*/
    #/*-------------------------------------------------------------*/
    #/* eigen vectors */
    z = numpy.zeros((r,r))
    irf = 0
    for k in range(8):
        for ir1 in range(irf,irf+irk[k]):
            for ir2 in range(irf,irf+irk[k]):
                z[ir2][ir1] = eigvect[k][ir2-irf][ir1-irf]
        for ir1 in range(irk[k]+irf,r):
            for ir2 in range(irf,irf+irk[k]):
                z[ir2][ir1] = 0.0
        irf += irk[k]

    #/* sort eigenfrequencies */
    wsort = scipy.zeros(r)
    i = 0
    for k in range(8):
        for ir1 in range(irk[k]):
            wsort[i] = eigvals[k][ir1]
            i += 1
    indice = numpy.argsort(wsort)
    wsort.sort()

    for i in range(len(wsort)):
        if wsort[i] > 0:
            x = math.sqrt(wsort[i]) / (2.0 * scipy.pi)
            if x > 0.00001:
                wsort[i] = x
            else:
                wsort[i] = 0.0
        else:
            wsort[i]= 0.0
  
    # output
    freqfile = open(freqs, 'w')
    y = []
    ifw = xindex(wsort, freqmin, 0)
    ifw += 1
    iw = ifw
    for i in range(ndata):
        try:
            y.append(wsort[iw])
        except IndexError:
            print('IndexError in wsort with iw = {}'.format(iw))
            sys.exit(-1)
        else:
            print('f{0}={1:.6f}'.format(i + 1, y[i]))
            # write predicted frequencies to file predictedf */
            freqfile.write('{}'.format(y[i]))
            iw += 1
    freqfile.close()

    # compute dyda
    dyda = compute_dyda(ns,hextype,r,tabs,d1,d2,d3,shape,ifw,ndata,z,wsort,indice)

    return y, dyda
  


#/* ------------------------------------------------------------------- */
#/* ---------------------------- MRQMIN ------------------------------- */
#/* ------------------------------------------------------------------- */
#/* ------------------------- Description from: ----------------------- */
#/* -------- Numerical Recipes: the art of scientific computing ------- */
#/* --W. H. Press, B. P. Flannery, S. A. Teukolsky, W. T, Vetterling -- */
#/* ------------------------------------------------------------------- */
#
#/* ------------------------------------------------------------------- */
#/* Subroutine MRQMIN(X, Y, SIG, NDATA, A, MA, LISTA, MFIT,
# * COVAR, ALPHA, NCA, CHISQ, FUNCS, ALAMDA)
# * Levenberg-Marquardt method, attemping to reduce the value of chisq of a
# * fit between a set of NDATA points X(I), Y(I) with individual standard 
# * deviations SIG(I), and a nonlinear function dependent of MA coefficients
# * A. The array LISTA numbers the parameters A such that the first MFIT 
# * correspond to values actually being adjusted; the remaining MA-MFIT
# * parameters are held fixed at their input value. The program returns
# * current best-fit values for the MA fit parameters A and CHISQ. The 
# * arrays COVAR(NCA, NCA) and ALPHA(NCA, NCA) with physical dimension NCA
# * are used as working space during most iterations. Supply a subroutine
# * FUNCS(X, A, YFIT, DYDA, MA) that evaluates the fitting function YFIT,
# * and its derivative DYDA with respect to the fittng parameters A at X.
# * On the first call provide an initial guess for the parameters A, and 
# * set ALAMDA<0 for initialization (which then sets ALAMDA=0.001). If the
# * step succedds CHISQ becomes smaller and ALAMDA decreases by a factor 
# * of 10. If the step fails ALAMDA grows by a factor of 10. You must call
# * this routine repeatedly until convergence is achieved. Then, make one
# * final call with ALAMDA=0, so that COVAR(I,J) returns the covariance
# * matrix, and ALPHA(I, J) the curvature matrix. */
#/* ------------------------------------------------------------------- */ 
#
#/* This is the optimisation routine which is called by MAIN once every iteration */
#/* mrqmin(d,r,tabs,
#      irk,d1,d2,d3,rho,shape,freqmin,
#      y,sig,ndata,guess,ia,ns,covar,alpha,&chisq, hextype, formod,&alamda) */
#
#/* ------ */
#/* Inputs */
#/* ------ */
#
#/* d  = order of polynomial fit eg) 8, 10 or 12*/
#/* r = dimension of problem. Related to d by  r= 3*(d+1)*(d+2)*(d+3)/6 */
#
#/* tabs = { itab, ltab, mtab, ntab }
#/* *itab, *ltab, *mtab, *ntab = 1D array's of type int. Related to r. _tab=alloc1int(r) */
#/* *irk = 1D array on int. irk = alloc1int(8)*/
#
#/* d1, d2, d3 = dimensions of sample, diameter, height */
#/* rho = density in g/cm^3 */
#/* shape = cylinder, sphere or rectangular parallelepiped */
#/* freqmin = minimum frequency, from param_data */
#
#/* y = 1D array of measured frequency data*/
#/* sig = 1D array of weightings - should be individual standard deviations for each freq? Is this an issue? */
#/* ndata = number of data points - frequencies used from freq_data */
#/* a = initial guess of parameter (cij) values. From param_data. Same size as ns */
#
#/* ia = 1D array of length ndata with entries = 1. This numbers the parameters such that the first MFIT parameters are adjusted and the remaining parameters are held constant */
#/* */
#
#/* ma = number of coefficients. Is equivalent to ns */
#/* covar = covariance matrix. Of size ns by ns (number of cijs). Initialised as identity matrix */
#/* alpha = curvature matrix. Of size ns by ns (number of cijs). Initialised as identity matrix */
#/* chisq = the difference between measured and predicted frequencies. Is not a "traditional" chisq */
#/* hextype = differentiates between VTI and HTI symmetry in the hexagonal case */
#/* alamda = parameter from conjugate-gradient method. Starts as <0 to initialise the routine and is changed in subsequent iterations */
#
def mrqmin(d,r,tabs,irk,d1,d2,d3,rho,shape,freqmin,y,sig,ndata,cxx_values,ia,ma,covar,alpha,hextype,alamda):
    # Loop is called if almada <0.
    # This initializes the routine.
    # Sets almada = -1.0 in main before calling MRQMIN.
    if alamda < 0.0:
        # create 1D arrays the size of the number of cxx values.
        beta = numpy.zeros(len(cxx_values))
        da   = numpy.zeros(len(cxx_values))

        # mfit is the number of cijs that are adjusted.
        # The remaining (ma = ns) - mfit cij values are left unchanged.
        # Set mfit = 0. Times looped through = number of independent cijs.
        mfit = 0
        for j in range(ma):
            if ia[j] > 0:
                mfit += 1

        # allocate a 2-d array of doubles - row vector the size of mfit?
        oneda = []

        # Set alamda to a small positive value (0.001)
        # after the routine has been initialized by the negative value
        alamda = 0.001

        # Compute "chisq" - need to update to formal chisq.
        chisq = mrqcof(d,r,tabs,irk,d1,d2,d3,rho,shape,freqmin,y,sig,ndata,cxx_values,ia,ma,alpha,beta,hextype)

        cxx_try = cxx_values.copy()
        # update chisq value
        ochisq = chisq
  
    # mfit started = 0 and then increased in the prior if loop, but mfit <= ns
    for j in range(mfit):
        # Set components in covariance matrix as equal to curvature matrix.
        # covar and alpha started as identity matrices.
        # Must be changed in mrqcof() otherwise this line would not do anything.
        for k in range(mfit):
            covar[j][k] = alpha[j][k]
        # change the main diagonals
        covar[j][j] = alpha[j][j] * (1.0 + alamda)
        # update oneda values by beta - which is changed (?) by mrqcof()
        oneda.append([beta[j]])
  
    gaussj(covar,mfit,oneda,1)
    for j in range(mfit):
        da[j] = oneda[j][0]

    # This is the stopping criteria - but how do we get alamda = 0.0?
    if alamda == 0.0:
        covsrt(covar,ma,ia,mfit)
        covsrt(alpha,ma,ia,mfit)
        return

    j = 0
    for l in range(ma):
        if ia[l] != 0:
            k = sorted(cxx_values.keys())[l]
            cxx_try[k] = cxx_values[k] + da[j]
            j += 1

    # Compute "chisq" - need to update to formal chisq
    chisq = mrqcof(d,r,tabs,irk,d1,d2,d3,rho,shape,freqmin,y,sig,ndata,cxx_try,ia,ma,covar,da,hextype)

    # if step succeeds value of chisq decreases: ochisq < chisq
    if chisq < ochisq:
        # decrease alamda by a factor of ten
        alamda *= 0.1
        # update chisq with the new, reduced, value
        ochisq = chisq 
        for j in range(mfit):
            for k in range(mfit):
                alpha[j][k] = covar[j][k]
            beta[j] = da[j]
        for l in range(ma):
            k = sorted(cxx_try.keys())[l]
            cxx_values[k] = cxx_try[k]

    # else step does not succeed and chisq increases
    else:
        # Increase alamda by a factor of ten
        # and then loop back and try again
        alamda *= 10.0
        chisq = ochisq



def make_cm(a, hextype=None):
    num_values = len(a)

    if num_values == 2: return __make_cm_isotropic(a)
    if num_values == 3: return __make_cm_cubic(a)
    if num_values == 5:
        if hextype == 1: return __make_cm_hexagonal_vti(a)
        if hextype == 2: return __make_cm_hexagonal_hti(a)
        raise ValueError('hextype value must be 1 or 2')
    if num_values == 6: return __make_cm_tetragonal(a)
    if num_values == 9: return __make_cm_orthohombic(a)
    err_msg = 'passed list of length {}'.format(len(a))
    raise ValueError(err_msg)



def __make_cm_isotropic(a):
    cm = [[0.0 for i in range(6)] for j in range(6)]
    try:
        cm[0][0] = a['c11'];
        cm[3][3] = a['c44'];
    except KeyError:
        raise
    else:
        cm[1][1] = cm[2][2] = cm[0][0]
        cm[4][4] = cm[5][5] = cm[3][3]
        cm[0][1] = cm[0][2] = cm[1][2] = cm[0][0] - 2.0 * cm[3][3]
        cm[1][0] = cm[2][0] = cm[2][1] = cm[0][0] - 2.0 * cm[3][3]
        return cm



def __make_cm_cubic(a):
    cm = [[0.0 for i in range(6)] for j in range(6)]
    try:
        cm[0][0] = a['c11']
        cm[0][1] = a['c12']
        cm[3][3] = a['c44']
    except KeyError:
        raise
    else:
        cm[1][1] = cm[2][2] = cm[0][0]
        cm[4][4] = cm[5][5] = cm[3][3]
        cm[0][2] = cm[1][2] = cm[0][1]
        cm[2][0] = cm[2][1] = cm[1][0] = cm[0][1]
        return cm



def __make_cm_hexagonal_vti(a):
    cm = [[0.0 for i in range(6)] for j in range(6)]
    try:
        cm[2][2] = a['c33']
        cm[1][2] = a['c23']
        cm[0][1] = a['c12']
        cm[3][3] = a['c44']
        cm[5][5] = a['c66']
    except KeyError:
        raise
    else:
        cm[0][0] = cm[1][1] = 2.0 * cm[5][5] + cm[0][1]
        cm[0][2] = cm[2][0] = cm[2][1] = cm[1][2]
        cm[1][0] = cm[0][1]
        cm[4][4] = cm[3][3]
        return cm



def __make_cm_hexagonal_hti(a):
    cm = [[0.0 for i in range(6)] for j in range(6)]
    try:
        cm[0][0] = a['c11']
        cm[2][2] = a['c33']
        cm[0][1] = a['c12']
        cm[5][5] = a['c66']
        cm[3][3] = a['c44']
    except KeyError:
        raise
    else:
        cm[1][2] = cm[2][1] = cm[2][2] - 2.0 * cm[3][3]
        cm[0][2] = cm[1][0] = cm[2][0] = cm[0][1]
        cm[1][1] = cm[2][2]
        cm[4][4] = cm[5][5]
        return cm



def __make_cm_tetragonal(a):
    cm = [[0.0 for i in range(6)] for j in range(6)]
    try:
        cm[0][0] = a['c11']
        cm[2][2] = a['c33']
        cm[1][2] = a['c23']
        cm[0][1] = a['c12']
        cm[3][3] = a['c44']
        cm[5][5] = a['c66']
    except KeyError:
        raise
    else:
        cm[1][1] = cm[0][0]
        cm[0][2] = cm[2][0] = cm[1][2]
        cm[1][0] = cm[0][1]
        cm[2][1] = cm[1][2]
        cm[4][4] = cm[3][3]
        return cm



def __make_cm_orthorhombic(a):
    cm = [[0.0 for i in range(6)] for j in range(6)]
    try:
        cm[0][0] = a['c11']
        cm[1][1] = a['c22']
        cm[2][2] = a['c33']
        cm[1][2] = a['c23']
        cm[0][2] = a['c13']
        cm[0][1] = a['c12']
        cm[3][3] = a['c44']
        cm[4][4] = a['c55']
        cm[5][5] = a['c66']
    except KeyError:
        raise
    else:
        cm[2][0] = cm[0][2]
        cm[1][0] = cm[0][1]
        cm[2][1] = cm[1][2]
        return cm


def volintegral(d1, d2, d3, l, m, n, shape):

    global _memo_vol_max
    global _memo_volintegral

# It is assumed that l, m, and n are all even numbers.
# Use the following code to check if necessary.

#    if l % 2 == 1 or m % 2 == 1 or n % 2 == 1:
#        return 0.0

    hl = l//2
    hm = m//2
    hn = n//2
    small = hl < _memo_vol_max and hm < _memo_vol_max and hn < _memo_vol_max
    
    if small and _memo_volintegral[hl][hm][hn]:
        return _memo_volintegral[hl][hm][hn]

    # ell. cylinder shape
    if shape == 1:
        ds = d1**(l+1) * d2**(m+1) * d3**(n+1)
        df_lm = doublefact(l-1) * doublefact(m-1)
        result = 4.0 * scipy.pi * ds / (n+1) * df_lm / doublefact(l+m+2)

    # spheroid shape
    elif shape == 2:
        ds = d1**(l+1) * d2**(m+1) * d3**(n+1)
        df_lm = doublefact(l-1) * doublefact(m-1)
        df_all = doublefact(l+m+n+3)
        result = 4.0 * scipy.pi * ds * df_lm * doublefact(n-1) / df_all

    # rp shape
    else:
        result = 8.0 / ((l+1) * (m+1) * (n+1)) * ds

    if small:
        _memo_volintegral[hl][hm][hn] = result

    return result



def doublefact(n):
    global _memo_doublefact
    global _memo_max

    if n == -1:
        return 1
    if _memo_doublefact[n]:
        return _memo_doublefact[n]
    if n < _memo_max:
        _memo_doublefact[n] = n * doublefact(n-2)
        return _memo_doublefact[n]
    else:
        return n * doublefact(n-2)



def e_fill(tabs, r, d1, d2, d3, rho, shape, irk):
	e = [scipy.zeros((irk[i],irk[i])) for i in range(8)]
	for k in range(8):
		irs = 0
		for ik in range(k):
			irs += irk[ik]
		irf = irs + irk[k]

		irv = 0
		ir1 = irs
		while ir1 < irf:
			irh = 0
			ir2 = irs
			while ir2 < irf:
				[i1,l1,m1,n1] = tabs[ir1]
				[i2,l2,m2,n2] = tabs[ir2]
				l = l1 + l2
				m = m1 + m2
				n = n1 + n2
				if i1 != i2:
					e[k][irv][irh] = 0.0
				else:
					e[k][irv][irh] = rho * volintegral(d1, d2, d3, l, m, n, shape);
				ir2 += 1
				irh += 1
			ir1 += 1
			irv += 1
	return e

def stiffness(cm):
	c = scipy.zeros((3,3,3,3))
	for i in range(3):
		for j in range(3):
			if i == 0 and j == 0:
				a = 0
			elif i == 1 and j == 1:
				a = 1
			elif i == 2 and j == 2:
				a = 2
			elif (i == 1 and j == 2) or (i == 2 and j == 1):
				a = 3
			elif (i == 0 and j == 2) or (i == 2 and j == 0):
				a = 4
			else:
				a = 5
			for k in range(3):
				for l in range(3):
					if k == 0 and l == 0:
						b = 0
					elif k == 1 and l == 1:
						b = 1
					elif k == 2 and l == 2:
						b = 2
					elif (k == 1 and l == 2) or (k == 2 and l == 1):
						b = 3
					elif (k == 0 and l == 2) or (k == 2 and l == 0):
						b = 4
					else:
						b = 5
					c[i][j][k][l] = cm[a][b]
	return c

def gamma_fill(tabs, r, d1, d2, d3, cm, shape, irk):
    gamma = [scipy.zeros((irk[i],irk[i])) for i in range(8)]
    c = stiffness(cm)
    for k in range(8):
        irs = sum(irk[0:k])
        irf = irs + irk[k]
        irv = 0
        for ir1 in range(irs,irf):
            irh = 0
            tabs1 = tabs[ir1]
            for ir2 in range(irs,irf):
                tabs2 = tabs[ir2]
                gamma_helper(gamma[k],c,tabs1,tabs2,irv,irh,d1,d2,d3,shape)
                irh += 1
            irv += 1
    return gamma

def xindex(ax, x, index):
    # Copyright (c) Colorado School of Mines, 2011.
    # All rights reserved. 

    # Author:  Dave Hale, Colorado School of Mines, 12/25/89
    # Translated to Python: Paul Freeman, University of Auckland, 6/11/2015

    nx = len(ax)

    # initialize lower and upper indices and step
    lower = index
    if lower < 0:
        lower = 0
    if lower >= nx:
        lower = nx - 1
    upper = lower + 1
    step = 1

    # if x values increasing
    if ax[-1] > ax[0]:
        # find indices such that ax[lower] <= x < ax[upper]
        while lower > 0 and ax[lower] > x:
            upper = lower
            lower -= step
            step += step
        if lower < 0:
            lower = 0;
        while upper < nx and ax[upper] <= x:
            lower = upper
            upper += step
            step += step
        if upper > nx:
            upper = nx

        # find index via bisection
        middle = (lower + upper) // 2
        while middle != lower:
            if x >= ax[middle]:
                lower = middle
            else:
                upper = middle
            middle = (lower + upper) // 2

    # else, if not increasing
    else:
        # find indices such that ax[lower] >= x > ax[upper]
        while lower > 0 and ax[lower] < x:
            upper = lower
            lower -= step
            step += step
        if lower < 0:
            lower = 0;
        while upper < nx and ax[upper] >= x:
            lower = upper
            upper += step
            step += step
        if upper > nx:
            upper = nx

        # find index via bisection
        middle = (lower + upper) // 2
        while middle != lower:
            if x <= ax[middle]:
                lower = middle
            else:
                upper = middle
            middle = (lower + upper) // 2

    return lower



def tabs_add(tabs, ir, irk, i, l, m, n):
    tabs[ir] = [i,l,m,n]
    return ir + 1, irk + 1



def index_relationship(d, r):
    tabs = numpy.zeros((int(r),4), dtype=numpy.int64)
    irk  = [0 for i in range(8)]

    ir = 0
    # k == 0
    for i in range(3):
        for l in range(d+1):
            for m in range(d-l+1):
                for n in range(d-l-m+1):
                    if (i == 0 and l % 2 == 0 and m % 2 == 0 and n % 2 == 0) or \
                       (i == 1 and l % 2 == 1 and m % 2 == 1 and n % 2 == 0) or \
                       (i == 2 and l % 2 == 1 and m % 2 == 0 and n % 2 == 1):
                        ir, irk[0] = tabs_add(tabs, ir, irk[0], i, l, m, n)
    # k == 1
    for i in range(3):
        for l in range(d+1):
            for m in range(d-l+1):
                for n in range(d-l-m+1):
                    if (i == 0 and l % 2 == 0 and m % 2 == 0 and n % 2 == 1) or \
                       (i == 1 and l % 2 == 1 and m % 2 == 1 and n % 2 == 1) or \
                       (i == 2 and l % 2 == 1 and m % 2 == 0 and n % 2 == 0):
                        ir, irk[1] = tabs_add(tabs, ir, irk[1], i, l, m, n)
    # k == 2
    for i in range(3):
        for l in range(d+1):
            for m in range(d-l+1):
                for n in range(d-l-m+1):
                    if (i == 0 and l % 2 == 0 and m % 2 == 1 and n % 2 == 0) or \
                       (i == 1 and l % 2 == 1 and m % 2 == 0 and n % 2 == 0) or \
                       (i == 2 and l % 2 == 1 and m % 2 == 1 and n % 2 == 1):
                        ir, irk[2] = tabs_add(tabs, ir, irk[2], i, l, m, n)
    # k == 3
    for i in range(3):
        for l in range(d+1):
            for m in range(d-l+1):
                for n in range(d-l-m+1):
                    if (i == 0 and l % 2 == 0 and m % 2 == 1 and n % 2 == 1) or \
                       (i == 1 and l % 2 == 1 and m % 2 == 0 and n % 2 == 1) or \
                       (i == 2 and l % 2 == 1 and m % 2 == 1 and n % 2 == 0):
                        ir, irk[3] = tabs_add(tabs, ir, irk[3], i, l, m, n)
    # k == 4
    for i in range(3):
        for l in range(d+1):
            for m in range(d-l+1):
                for n in range(d-l-m+1):
                    if (i == 0 and l % 2 == 1 and m % 2 == 0 and n % 2 == 0) or \
                       (i == 1 and l % 2 == 0 and m % 2 == 1 and n % 2 == 0) or \
                       (i == 2 and l % 2 == 0 and m % 2 == 0 and n % 2 == 1):
                        ir, irk[4] = tabs_add(tabs, ir, irk[4], i, l, m, n)
    # k == 5
    for i in range(3):
        for l in range(d+1):
            for m in range(d-l+1):
                for n in range(d-l-m+1):
                    if (i == 0 and l % 2 == 1 and m % 2 == 0 and n % 2 == 1) or \
                       (i == 1 and l % 2 == 0 and m % 2 == 1 and n % 2 == 1) or \
                       (i == 2 and l % 2 == 0 and m % 2 == 0 and n % 2 == 0):
                        ir, irk[5] = tabs_add(tabs, ir, irk[5], i, l, m, n)
    # k == 6
    for i in range(3):
        for l in range(d+1):
            for m in range(d-l+1):
                for n in range(d-l-m+1):
                    if (i == 0 and l % 2 == 1 and m % 2 == 1 and n % 2 == 0) or \
                       (i == 1 and l % 2 == 0 and m % 2 == 0 and n % 2 == 0) or \
                       (i == 2 and l % 2 == 0 and m % 2 == 1 and n % 2 == 1):
                        ir, irk[6] = tabs_add(tabs, ir, irk[6], i, l, m, n)
    # k == 7
    for i in range(3):
        for l in range(d+1):
            for m in range(d-l+1):
                for n in range(d-l-m+1):
                    if (i == 0 and l % 2 == 1 and m % 2 == 1 and n % 2 == 1) or \
                       (i == 1 and l % 2 == 0 and m % 2 == 0 and n % 2 == 1) or \
                       (i == 2 and l % 2 == 0 and m % 2 == 1 and n % 2 == 0):
                        ir, irk[7] = tabs_add(tabs, ir, irk[7], i, l, m, n)
    print("irk[0]=" + str(irk[0]))
    print("irk[1]=" + str(irk[1]))
    print("irk[2]=" + str(irk[2]))
    print("irk[3]=" + str(irk[3]))
    print("irk[4]=" + str(irk[4]))
    print("irk[5]=" + str(irk[5]))
    print("irk[6]=" + str(irk[6]))
    print("irk[7]=" + str(irk[7]))

    return tabs, irk
