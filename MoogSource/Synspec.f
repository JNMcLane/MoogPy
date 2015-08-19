
      subroutine synspec ()
c******************************************************************************
c     This routine does synthetic spectra                                
c******************************************************************************

      implicit real*8 (a-h,o-z)
      include 'Atmos.com'
      include 'Linex.com'
      include 'Factor.com'
      include 'Pstuff.com'
      include 'Dummy.com'
      real*8 dd(5000)

cf2py intent(callback, hide) recorder
      external recorder

c*****initialize the synthesis
      write (nf1out,1101)
      write (nf2out,1002) moditle(1:73)
      if (iunits .eq. 1) then
         write (nf2out,1103) oldstart,oldstop,oldstep,olddelta
      else
         write (nf2out,1102) start,sstop,step,delta
      endif
      if (iraf .eq. 1) then
         npoint = (sstop-start)/step
         write (nf4out,1104) npoint,wave,wave,step,step
         write (nf4out,1105)
         write (nf4out,1106) moditle
         do j=1,93
            if (pec(j) .gt. 0 ) then
               dummy1(j) = dlog10(xabund(j)) + 12.0
               write (nf4out,1107) names(j),dummy1(j)
            endif
         enddo
         write (nf4out,1108) vturb(1)
         write (nf4out,1109)
      endif
      n = 1           
      num = 0
      nsteps = 1
      if (mode .ne. 4) then 
         lim1line = 0
         lim2line = 0
         lim1obs = 0
         lim2obs = 0
         lim1 = 0
         lim2 = 0
      endif


c*****calculate continuum quantities at the spectrum wavelength
      wave = start
      wavl = 0.
30    if (dabs(wave-wavl)/wave .ge. 0.001) then
         wavl = wave   
         call opacit (2,wave)    
         if (modprintopt .ge. 2) 
     .       write (nf1out,1001) wave,(kaplam(i),i=1,ntau)
         call cdcalc (1)  
         first = 0.4343*cd(1)
         flux = rinteg(xref,cd,dummy1,ntau,first)
         if (iunits .eq. 1) then
            write (nf1out,1003) 1.d-4*wave,flux
         else
            write (nf1out,1004) wave,flux
         endif
      endif


c*****find the appropriate set of lines for this wavelength, reading 
c     in a new set if needed
      if (mode .eq. 3) then
20       call linlimit
         if (lim2line .lt. 0) then
            call inlines (2)
            call nearly (1)
            go to 20
         endif
         lim1 = lim1line
         lim2 = lim2line
      endif


c*****compute a spectrum depth at this point
      call taukap   
      call cdcalc (2)
      first = 0.4343*cd(1)
      d(n) = rinteg(xref,cd,dummy1,ntau,first)
c      write (*,*) wave, d(n), first
      write (*,*) wave, lim1, lim2
      call recorder(wave, d(n))
c      call recorder()
      if (mod(n,10) .eq. 0) then
         if (iraf .eq. 1) then
            do j=1,10
               dd(num+j) = 1. - d(num+j)
            enddo
            write (nf4out,1110) (dd(num+j),j=1,10)
         endif
         if (iunits .eq. 1) then
            wave3 = 1.d-4*(wave - 9.0*step)
            write (nf1out,1112) wave3,(d(num+j),j=1,10)
         else
            wave3 = wave - 9.0*step
            write (nf1out,1111) wave3,(d(num+j),j=1,10)
         endif
         if (nf2out .gt. 0) write (nf2out,1110) (d(num+j),j=1,10)
         num = num + 10
      endif


c*****step in wavelength and try again 
      wave = oldstart + step*nsteps
      if (wave .le. sstop) then
         n = n + 1        
         nsteps = nsteps + 1
         if (n .gt. 5000) then
            n = 1                                      
            num = 0
         endif
         go to 30                   


c*****finish the synthesis
      else
         nn = mod(n,10)
         if (nn .ne. 0) then
            if (iraf .eq. 1) then
               do j=1,nn
                  dd(num+j) = 1. - d(num+j)
               enddo
               write (nf4out,1110) (dd(num+j),j=1,nn)
            endif
            if (iunits .eq. 1) then
               wave3 = 1.d-4*(wave - 9.0*step)
               write (nf1out,1112) wave3,(d(num+j),j=1,nn)
            else
               wave3 = wave - 9.0*step
               write (nf1out,1111) wave3,(d(num+j),j=1,nn)
            endif
            if (nf2out .gt. 0) write (nf2out,1110) (d(num+j),j=1,nn)
         endif
         if (iunits .eq. 1) then
            write (nf1out,1113) 1.d-4*wave
         else
            write (nf1out,1114) wave
         endif
         return 
      endif


c*****format statements
1001  format ('  kaplam from 1 to ntau at wavelength',f10.2/
     .        (6(1pd12.4)))
1002  format ('MODEL: ',a73)
1003  format ('AT WAVELENGTH/FREQUENCY =',f11.7,
     .        '  CONTINUUM FLUX/INTENSITY =',1p,d12.5)
1004  format ('AT WAVELENGTH/FREQUENCY =',f11.3,
     .        '  CONTINUUM FLUX/INTENSITY =',1p,d12.5)
1101  format (/'SPECTRUM DEPTHS')
1102  format (4f11.3)
1103  format (4f10.7)
1104  format ('SIMPLE  =    t'/'NAXIS   =     1'/'NAXIS1  = ',i10,/
     .        'W0      =',f10.4/'CRVAL1  =',f10.4/'WPC     =',f10.4/
     .        'CDELT1  =',f10.4)
1105  format (16HORIGIN  = 'moog'/21HDATA-TYP= 'synthetic'/
     .        18HCTYPE1  = 'lambda'/21HCUNIT1  = 'angstroms')
1106  format (11HTITLE   = ',A65,1H')
1107  format ('ATOM    = ',1H',7x,a2,1H',/,'ABUND   = ',f10.2)
1108  format ('VTURB   = ',d10.4,'     /  cm/sec  ')
1109  format ('END')
1110  format (10f7.4)
1111  format (f10.3,': depths=',10f6.3)
1112  format (f10.7,': depths=',10f6.3)
1113  format ('FINAL WAVELENGTH/FREQUENCY =',f10.7/)
1114  format ('FINAL WAVELENGTH/FREQUENCY =',f10.3/)


      end                                




