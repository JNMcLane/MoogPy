f2py -c MoogStokessilent.f -m MoogStokesPy -L/usr/lib/atlas/ -llapack Begin.f Infile.f Getasci.f Nansi.f Getcount.f Synth.f Synspec.f Finish.f Opacit.f OpacHydrogen.f OpacHelium.f Opacmetals.f Opacscat.f Opaccouls.f Nearly.f Eqlib.f Partnew.f Cdcalc.f Jexpint.f Linlimit.f Prinfo.f Sunder.f Gammabark.f Rinteg.f Batom.f Bmolec.f Inlines.f Params.f Putasci.f Taukap.f Voigt.f Discov.f Inmodel.f Partfn.f Damping.f Ucalc.f Invert.f Trudamp.f Lineinfo.f SynStokes.f Spline.f SplineDriver.f WaveGrid.f Curfit.f CalcGeom.f DELOQuad.f CalcOpacities.f ComplexVoigt.f
cp MoogStokesPy.so ../MoogTools/
