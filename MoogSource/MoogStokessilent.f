
      subroutine moogstokessilent
c******************************************************************************
c     This is the main driver for MOOG.  It reads the parameter
c     file and sends MOOG to various controlling subroutines.
c     This is the normal interactive version of the code; for batch
c     processing without user decisions, run MOOGSILENT instead.
c******************************************************************************

      include 'Atmos.com'
      include 'Pstuff.com'

c     MoogStokesSilent - version 0.95
c         Friday 23 Oct 2015
      moogversion='0.95'

c$$$$$$$$$$$$$$$$$$$$$$$$ USER SETUP AREA $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
c*****in compiling MOOG, here the various machine-specific things are 
c     declared.  First, define the directory where MOOG lives, in order to 
c     be able to pull in auxiliary data files; executing 'make' will 
c     generate a reminder of this necessity
c      write (moogpath,1001)
c      moogpath = 
c     .  '/home/deen/Code/Python/MoogPy/MoogSource/'
c      write (*,*) moogpath


c*****What kind of machine are you using?  Possible ones are:
c     "mac" = Intel-based Apple Mac 
c     "pcl" = a PC or desktop running some standard linux like Redhat
c     "uni" = a machine running Unix, specifically Sun Solaris
      machine = "pcl"


c*****for x11 terminal types, define the parameters of plotting windows;
c     set up an x11 screen geometry and placement that is good for spectrum
c     syntheses (long, but not tall); the user should play with the format
c     statements for particular machines.
c      write (smt1,1018)
c     now do the same for line abundance trend plots (short but tall).
c      write (smt2,1017)
c$$$$$$$$$$$$$$$$$$$$$$$ END OF USER SETUP $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$


c*****declare this to be the normal interactive version; variable "silent"
c     will be queried on all occasions that might call for user input;
c     DON'T CHANGE THIS VARIABLE; 
c     if silent = 'n', the normal interactive MOOG is run;
c     if silent = 'y', the non-interactive MOOG is run
      silent = 'y'


c*****invoke the overall starting routine
      control = '       '
      call begin


c*****use one of the standard driver routines ("isotop" is obsolete):
c      if     (control .eq. 'synplot') then
c         call plotit
      if (control .eq. 'synth  ') then
         call synth
c      elseif (control .eq. 'cogsyn ') then
c         call cogsyn  
c      elseif (control .eq. 'blends ') then
c         call blends  
c      elseif (control .eq. 'abfind ') then
c         call abfind
c      elseif (control .eq. 'ewfind ') then
c         call ewfind
c      elseif (control .eq. 'cog    ') then
c         call cog
c      elseif (control .eq. 'calmod ') then
c         call calmod
c      elseif (control .eq. 'doflux ') then
c         call doflux   
c      elseif (control .eq. 'weedout') then
c         call weedout  
c      elseif (control .eq. 'gridsyn') then
c         call gridsyn  
c      elseif (control .eq. 'gridplo') then
c         call gridplo  
c      elseif (control .eq. 'binary ') then
c         call binary
c      elseif (control .eq. 'abpop  ') then
c         call abpop
c      elseif (control .eq. 'synpop ') then
c         call synpop
      elseif (control .eq. 'stoktra') then
          call stokestrace
      elseif (control .eq. 'synstok') then
         call synstokes


c*****or, put in your own drivers in the form below....
c      elseif (control .eq. 'mine  ') then
c         call  mydriver 


c*****or else you are out of luck!
      else
         array = 'THIS IS NOT ONE OF THE DRIVERS.  TRY AGAIN (y/n)?'
      endif

      rewind nfparam


c*****format statements
1001  format (60(' '))
1002  format ('The "isotop" driver is obsolete; "synth" does ',
     .        'its functions now!')
1003  format (22x,'MOOG IS CONTROLLED BY DRIVER ',a7)
1017  format ('x11 -bg black -title MOOGplot -geom 700x800+650+000')
1018  format ('x11 -bg black -title MOOGplot -geom 1200x350+20+450')


      end


      
