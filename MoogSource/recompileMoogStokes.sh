f2py --f77flags=-fcheck=all -c MoogStokesPy.pyf MoogStokessilent.f  -L/usr/lib64/atlas/ -llapack -lf77blas -latlas -lcblas Begin.f Infile.f Getasci.f Nansi.f Getcount.f Synth.f Synspec.f Finish.f Opacit.f OpacHydrogen.f OpacHelium.f Opacmetals.f Opacscat.f Opaccouls.f Nearly.f Eqlib.f Partnew.f Cdcalc.f Jexpint.f Linlimit.f Prinfo.f Sunder.f Gammabark.f Rinteg.f Batom.f Bmolec.f Inlines.f Params.f Putasci.f Taukap.f Voigt.f Discov.f Inmodel.f Partfn.f Damping.f Ucalc.f Invert.f Trudamp.f Lineinfo.f SynStokes.f Spline.f SplineDriver.f WaveGrid.f Curfit.f CalcGeom.f DELOQuad.f CalcOpacities.f ComplexVoigt.f StokesTrace.f StokesDipStick.f
cp MoogStokesPy.so ../MoogTools/
