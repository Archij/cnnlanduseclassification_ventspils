# -*- coding: utf-8 -*-
"""
@author: Arthur Stepchenko
"""
import numpy as np

def  VMD_2D(f, alpha, tau, K, DC, init, tol):
    """
    u,u_hat,omega = VMD_2D(f, alpha, tau, K, DC, init, tol)
    2D Variational mode decomposition
    code based on Dominique Zosso's MATLAB code, available at:
    https://se.mathworks.com/matlabcentral/fileexchange/45918-two-dimensional-variational-mode-decomposition
    Original paper:
    Dragomiretskiy, K. and Zosso, D. (2014) ‘Variational Mode Decomposition’, 
    IEEE Transactions on Signal Processing, 62(3), pp. 531–544. doi: 10.1109/TSP.2013.2288675.
    
    
    Input and Parameters:
    ---------------------
    signal     - the space domain signal (2D) to be decomposed
    alpha      - the balancing parameter for data fidelity constraint
    tau        - time-step of dual ascent ( pick 0 for noise-slack )
    K          - the number of modes to be recovered
    DC         - true, if the first mode is put and kept at DC (0-freq)
    init       - 0 = all omegas start at 0
                 1 = all omegas start initialized randomly
    tol        - tolerance of convergence criterion; typically around 1e-7
 
    Output:
    -------
    u       - the collection of decomposed modes
    u_hat   - spectra of the modes
    omega   - estimated mode center-frequencies
    """

    # Resolution of image
    Hy = len(f)
    Hx = len(f[0])
    X,Y = np.meshgrid(np.arange(1,Hx+1)/Hx, np.arange(1,Hy+1)/Hy)

    # Spectral Domain discretization
    fx = 1./Hx
    fy = 1./Hy
    freqs_1 = X-0.5-fx
    freqs_2 = Y-0.5-fy
    
    # N is the maximum number of iterations (if not converged yet, then it won't anyway)
    N = 10
    
    # For future generalizations: individual alpha for each mode
    Alpha = alpha*np.ones((K,1))
    
    # Construct f_hat
    f_hat = np.fft.fftshift((np.fft.fft2(f)))
    
    # Storage matrices for (Fourier) modes. All iterations are not recorded.
    # matrix keeping track of every iterant // could be discarded for mem
    u_hat = np.zeros([K, Hy, Hx],dtype=complex)
    u_hat_old = np.array(u_hat)
       
    sum_uk = 0 # accumulator
     
    # Storage matrices for (Fourier) Lagrange multiplier.
    mu_hat = np.zeros([Hy, Hx],dtype=complex)

    # N iterations at most, 2 spatial coordinates, K clusters
    omega = np.zeros([K, N, 2])

    # Initialization of omega_k
    if init == 0:
        # spread omegas radially
        
        #if DC, keep first mode at 0,0
        if DC==1:
            maxK = K-1
        else:
            maxK = K

        for k in (DC+1,DC+maxK):
            omega[k-1,0,0] = 0.25*np.cos(np.pi*(k-1)/maxK)
            omega[k-1,0,1] = 0.25*np.sin(np.pi*(k-1)/maxK)
    # Case 1: random on half-plane
    elif init == 1:
        for k in (0,K-1):
            omega[k,0,0] = np.random.rand()-1/2
            omega[k,0,1] = np.random.rand()/2
        
        # DC component (if expected)
        if DC == 1:
            omega[0,0,0] = 0
            omega[0,0,1] = 0     

    # Main loop for iterative updates
    # Stopping criteria tolerances
    uDiff=tol+np.spacing(1)
    omegaDiff = tol+np.spacing(1)

    # first run
    n = 0
    
    # % run until convergence or max number of iteration
    while ((uDiff > tol or omegaDiff > tol) and  n < N-1): 
        
        # first things first
        k = 0
        
        # compute the halfplane mask for the 2D "analytic signal"
        HilbertMask = (np.sign(freqs_1*omega[k,n,0] + freqs_2*omega[k,n,1])+1)
        
        # update first mode accumulator
        sum_uk = u_hat[K-1,:,:] + sum_uk - u_hat[k,:,:]
        
        # update first mode's spectrum through wiener filter (on half plane)
        u_hat[k,:,:] = np.divide(np.multiply((f_hat - sum_uk - mu_hat[:,:]/2),HilbertMask), (1+Alpha[k]*((freqs_1 - omega[k,n,0])**2+(freqs_2 - omega[k,n,1])**2)))
        
        # update first mode's central frequency as spectral center of gravity
        if DC==0:
            omega[k,n+1,0] = np.sum(np.sum(np.multiply(freqs_1, (abs(u_hat[k,:,:])**2))))/np.sum(np.sum(abs(u_hat[k,:,:])**2))
            omega[k,n+1,1] = np.sum(np.sum(np.multiply(freqs_2, (abs(u_hat[k,:,:])**2))))/np.sum(np.sum(abs(u_hat[k,:,:])**2))
        
            # keep omegas on same halfplane
            if omega[k,n+1,1] < 0:
               omega[k,n+1,:] = -omega[k,n+1,:]
    
        # recover full spectrum from analytic signal
        u_hat[k,:,:] = np.fft.fftshift(np.fft.fft2(np.real(np.fft.ifft2(np.fft.ifftshift(np.squeeze(u_hat[k,:,:]))))))

        # work on other modes
        for k in np.arange(1,K):
        
            # recompute Hilbert mask
            HilbertMask = (np.sign(freqs_1*omega[k,n,0] + freqs_2*omega[k,n,1])+1)
        
            # update accumulator
            sum_uk = u_hat[k-1,:,:] + sum_uk - u_hat[k,:,:]
        
            # update signal spectrum
            u_hat[k,:,:] = np.divide(np.multiply((f_hat - sum_uk - mu_hat[:,:]/2), HilbertMask), (1+Alpha[k]*((freqs_1 - omega[k,n,0])**2+(freqs_2 - omega[k,n,1])**2)))
        
            # update signal frequencies
            omega[k,n+1,0] = np.sum(np.sum(np.multiply(freqs_1, (abs(u_hat[k,:,:])**2))))/np.sum(np.sum(abs(u_hat[k,:,:])**2))
            omega[k,n+1,1] = np.sum(np.sum(np.multiply(freqs_2, (abs(u_hat[k,:,:])**2))))/np.sum(np.sum(abs(u_hat[k,:,:])**2))
        
            # keep omegas on same halfplane
            if omega[k,n+1,1] < 0:
                omega[k,n+1,:] = -omega[k,n+1,:]
        
            # recover full spectrum from analytic signal
            u_hat[k,:,:] = np.fft.fftshift(np.fft.fft2(np.real(np.fft.ifft2(np.fft.ifftshift(np.squeeze(u_hat[k,:,:]))))))
        
               
        # Gradient ascent for augmented Lagrangian
        mu_hat[:,:] = mu_hat[:,:] + tau*(np.sum(u_hat,axis=0) - f_hat)
    
        # increment iteration counter
        n = n+1
    
        # convergence?
        uDiff = np.spacing(1)
        omegaDiff = np.spacing(1)
    
        for k in np.arange(0,K):
            omegaDiff = omegaDiff + np.sum(np.sum(abs(omega[:,n,:] - omega[:,n-1,:])**2))
            uDiff = uDiff + np.sum(np.sum(1/(Hx*Hy)*np.multiply((u_hat[k,:,:]-u_hat_old[k,:,:]), np.conj(u_hat[k,:,:]-u_hat_old[k,:,:]))))
            
        uDiff = abs(uDiff)
    
        u_hat_old = np.array(u_hat)
        
    # Signal Reconstruction
    # Inverse Fourier Transform to compute (spatial) modes
    u = np.zeros([K,Hy,Hx])
    for k in np.arange(0,K):
        u[k,:,:] = np.real(np.fft.ifft2(np.fft.ifftshift(np.squeeze(u_hat[k,:,:]))))

    # Should the omega-history be returned, or just the final results?
    #omega = omega[n,:,:]
    omega = omega[:,:n,:]
    
    return u, u_hat, omega