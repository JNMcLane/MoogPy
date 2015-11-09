import pyfits
import AstroUtils
import glob
import MoogTools
import SpectralTools
import numpy
import os

class Phrase( object ):
    def __init__(self, rawData=None, diskInt = 'BEACHBALL'):
        self.rawData = rawData
        self.wlStart = rawData[0].header.get('WLSTART')
        self.wlStop = rawData[0].header.get('WLSTOP')
        if diskInt == 'BEACHBALL':
            self.processedData = SpectralTools.BeachBall(parent=self)
        elif diskInt == 'DISKOBALL':
            self.processedData = SpectralTools.DiskoBall(parent=self)

    @classmethod
    def fromFile(self, hdr, data):
        rawData = []
        rawData.append(SpectralTools.Spectrum.from_file(hdr,data))
        return self(rawData=rawData)

    def addRawSpectrum(self, hdr, data):
        self.rawData.append(SpectralTools.Spectrum.from_file(hdr, data))

    def owns(self, hdr):
        if ((self.wlStart == hdr.get('WLSTART')) & 
                (self.wlStop == hdr.get("WLSTOP"))):
            return True
        return False

    def inWlRange(self, wlStart, wlStop):
        return ((self.wlStart < wlStop) & (self.wlStop > wlStart))

    #def integrate(self, vsini=0.0):
    #    self.processedData.diskInt(vsini=vsini)

    def rehearse(self, vsini=0.0, R=0):
        self.processedData.resample(vsini=vsini, R=R)

    def perform(self, vsini= 0.0, R = 0.0):
        return self.processedData.yank(vsini=vsini, R = R)

    def saveRaw(self, filename = None, primaryHeaderKWs={}):
        HDUs = []
        for spectrum in self.rawData:
            hdr = spectrum.header.copy()
            SpectrumHDU = pyfits.BinTableHDU.from_columns(spectrum.columns,
                    header=hdr)
            SpectrumHDU.name = "%.4fA - %.4fA PHI=%.3f MU=%.3f" % (hdr.get("wlStart"), hdr.get("wlStop"), hdr.get("PHI_ANGLE"), hdr.get("MU"))

            HDUs.append(SpectrumHDU)

        if filename == None:
            return HDUs

        if os.path.exists(filename):    #file exists!  get ready to append!
            while os.path.exists(filename+'.lock'):
                print("Gnarly dude!  The file is locked!  I'll just hang out here for a while and wait")
                time.sleep(0.1)
            with open(filename+'.lock', 'w'):
                os.utime(filename+'.lock', None)
            HDUList = pyfits.open(filename, mode='update')
            for spectrum in HDUs:
                try:
                    HDUList.pop(HDUList.index_of(spectrum.name))
                except:
                    pass
                HDUList.append(spectrum)
            HDUList.update_extend()
            HDUList.verify(option='silentfix')
            HDUList.close()
            os.remove(filename+'.lock')
        else:
            HDUList = pyfits.HDUList()
            primary = pyfits.PrimaryHDU()
            if primaryHeaderKWs != None:
                for key in primaryHeaderKWs.keys():
                    primary.header.set(key, primaryHeaderKWs[key])
            HDUList.append(primary)
            for spectrum in HDUs:
                HDUList.append(spectrum)
            HDUList.update_extend()
            HDUList.verify(option='silentfix')
            HDUList.writeto(filename)


    def saveInterpolated(self, filename = None, primaryHeaderKWs={}):
        HDUs = []
        for spectrum in self.processedData.interpolated:
            hdr = spectrum.header.copy()
            SpectrumHDU = pyfits.BinTableHDU.from_columns(spectrum.columns,
                    header=hdr)
            SpectrumHDU.name = "%.4fA - %.4fA PHI=%.3f MU=%.3f DELTAV=%.3f" % (hdr.get("wlStart"), hdr.get("wlStop"), hdr.get("PHI_ANGLE"), hdr.get("MU"), hdr.get('DELTAV'))

            HDUs.append(SpectrumHDU)

        if filename == None:
            return HDUs

        if os.path.exists(filename):    #file exists!  get ready to append!
            while os.path.exists(filename+'.lock'):
                print("Gnarly dude!  The file is locked!  I'll just hang out here for a while and wait")
                time.sleep(0.1)
            with open(filename+'.lock', 'w'):
                os.utime(filename+'.lock', None)
            HDUList = pyfits.open(filename, mode='update')
            for spectrum in HDUs:
                try:
                    HDUList.pop(HDUList.index_of(spectrum.name))
                except:
                    pass
                HDUList.append(spectrum)
            HDUList.update_extend()
            HDUList.verify(option='silentfix')
            HDUList.close()
            os.remove(filename+'.lock')
        else:
            HDUList = pyfits.HDUList()
            primary = pyfits.PrimaryHDU()
            if primaryHeaderKWs != None:
                for key in primaryHeaderKWs.keys():
                    primary.header.set(key, primaryHeaderKWs[key])
            HDUList.append(primary)
            for spectrum in HDUs:
                HDUList.append(spectrum)
            HDUList.update_extend()
            HDUList.verify(option='silentfix')
            HDUList.writeto(filename)

    def saveIntegrated(self, filename = None, primaryHeaderKWs={}):
        HDUs = []
        for spectrum in self.processedData.integrated:
            hdr = spectrum.header.copy()
            SpectrumHDU = pyfits.BinTableHDU.from_columns(spectrum.columns,
                    header=hdr)
            SpectrumHDU.name = "%.4fA - %.4fA VSINI=%.3f" % (hdr.get("wlStart"), hdr.get("wlStop"), hdr.get('VSINI'))

            HDUs.append(SpectrumHDU)

        if filename == None:
            return HDUs

        if os.path.exists(filename):    #file exists!  get ready to append!
            while os.path.exists(filename+'.lock'):
                print("Gnarly dude!  The file is locked!  I'll just hang out here for a while and wait")
                time.sleep(0.1)
            with open(filename+'.lock', 'w'):
                os.utime(filename+'.lock', None)
            HDUList = pyfits.open(filename, mode='update')
            for spectrum in HDUs:
                try:
                    HDUList.pop(HDUList.index_of(spectrum.name))
                except:
                    pass
                HDUList.append(spectrum)
            HDUList.update_extend()
            HDUList.verify(option='silentfix')
            HDUList.close()
            os.remove(filename+'.lock')
        else:
            HDUList = pyfits.HDUList()
            primary = pyfits.PrimaryHDU()
            if primaryHeaderKWs != None:
                for key in primaryHeaderKWs.keys():
                    primary.header.set(key, primaryHeaderKWs[key])
            HDUList.append(primary)
            for spectrum in HDUs:
                HDUList.append(spectrum)
            HDUList.update_extend()
            HDUList.verify(option='silentfix')
            HDUList.writeto(filename)

    def saveConvolved(self, filename = None, primaryHeaderKWs={}):
        HDUs = []
        for spectrum in self.processedData.convolved:
            hdr = spectrum.header.copy()
            SpectrumHDU = pyfits.BinTableHDU.from_columns(spectrum.columns,
                    header=hdr)
            SpectrumHDU.name = "%.4fA - %.4fA VSINI=%.3f R=%.1f" % (hdr.get("wlStart"), hdr.get("wlStop"), hdr.get('VSINI'), hdr.get('RESOLVING_POWER'))

            HDUs.append(SpectrumHDU)

        if filename == None:
            return HDUs

        if os.path.exists(filename):    #file exists!  get ready to append!
            while os.path.exists(filename+'.lock'):
                print("Gnarly dude!  The file is locked!  I'll just hang out here for a while and wait")
                time.sleep(0.1)
            with open(filename+'.lock', 'w'):
                os.utime(filename+'.lock', None)
            HDUList = pyfits.open(filename, mode='update')
            for spectrum in HDUs:
                try:
                    HDUList.pop(HDUList.index_of(spectrum.name))
                except:
                    pass
                HDUList.append(spectrum)
            HDUList.update_extend()
            HDUList.verify(option='silentfix')
            HDUList.close()
            os.remove(filename+'.lock')
        else:
            HDUList = pyfits.HDUList()
            primary = pyfits.PrimaryHDU()
            if primaryHeaderKWs != None:
                for key in primaryHeaderKWs.keys():
                    primary.header.set(key, primaryHeaderKWs[key])
            HDUList.append(primary)
            for spectrum in HDUs:
                HDUList.append(spectrum)
            HDUList.update_extend()
            HDUList.verify(option='silentfix')
            HDUList.writeto(filename)

class Melody( object ):
    def __init__(self, phrases = [], filename=None):
        self.phrases = []
        self.filename = filename
        self.loadMelody()
        self.muted = True
        self.nPhrases = len(self.phrases)

    def loadMelody(self):
        info = pyfits.info(self.filename, output='')
        self.nSpectra = len(info)-1
        self.header = pyfits.getheader(self.filename, ext=0)
        self.Teff = self.header.get("TEFF")
        self.logg = self.header.get("LOGG")
        self.B = self.header.get("BFIELD")

        for i in range(self.nSpectra):
            added = False
            hdr = pyfits.getheader(self.filename, ext=i+1)
            data = pyfits.getdata(self.filename, ext=i+1)
            for phrase in self.phrases:
                if phrase.owns(hdr):
                    phrase.addRawSpectrum(hdr, data)
                    added=True
                    break
            if not(added):
                self.phrases.append(Phrase.fromFile(hdr, data))

        for phrase in self.phrases:
            phrase.processedData.loadData()

    def addPhrase(self, phrases):
        for phrase in phrases:
            self.phrases.append(phrase)
        self.nPhrases = len(self.phrases)

    def selectPhrases(self, wlRange=[]):
        self.selectedPhrases = []
        for phrase in self.phrases:
            self.selectedPhrases.append(phrase.inWlRange(wlStart=wlRange[0],
                wlStop=wlRange[1]))

    def inParameterRange(self, TeffRange=[], loggRange=[], BfieldRange=[]):
        self.muted = False
        try:
            if ((self.Teff < TeffRange[0]) or (self.Teff > TeffRange[1])):
                self.muted = True
        except:
            pass
        try:
            if ((self.logg < loggRange[0]) | (self.logg > loggRange[1])):
                self.muted = True
        except:
            pass
        try:
            if ((self.B < BfieldRange[0]) | (self.B > BfieldRange[1])):
                self.muted = True
        except:
            pass

    def rehearse(self, vsini = 0.0, R = 0):
        for i in range(self.nPhrases):
            if self.selectedPhrases[i]:
                self.phrases[i].rehearse(vsini = vsini, R=R)

    def perform(self, vsini = 0.0, R = 0.0):
        spectra = []
        label = "Teff = %d K log g = %.2f Bfield = %.2f kG" % (self.Teff, self.logg, self.B)
        for i in range(self.nPhrases):
            if self.selectedPhrases[i]:
                spectra.append(self.phrases[i].perform(vsini=vsini, R=R))


        return spectra, label

    def record(self, filename=''):
        for i in range(self.nPhrases):
            if self.selectedPhrases[i]:
                self.phrases[i].record(filename)

class Score( object ):
    """
    
    """
    def __init__(self, melodies = [], directory=None):
        self.melodies = melodies
        self.directory = directory
        self.loadMelodies()

    def loadMelodies(self):
        melodyFiles = glob.glob(self.directory+'*raw.fits')
        for melody in melodyFiles:
            self.melodies.append(Melody(filename=melody))

    def setWlRange(self, wlStart, wlStop):
        for melody in self.melodies:
            melody.selectPhrases(wlStart, wlStop)

    #    self.Score.selectMelodies(TeffRange=self.TeffRange, loggRange=self.loggRange,
    #            BfieldRange=self.BfieldRange, self.wlRange)
    def selectMelodies(self, TeffRange = [], loggRange = [], BfieldRange=[],
            wlRange=[]):
        for melody in self.melodies:
            melody.inParameterRange(TeffRange=TeffRange,
                loggRange=loggRange, BfieldRange=BfieldRange)
            if not(melody.muted):
                melody.selectPhrases(wlRange=wlRange)

    def rehearse(self, vsini=0.0, R=0.0):
        '''
        Score.rehearse(vsini=0.0, R=0.0) - For the melodies and phrases selected by
             the parameter and wavelength ranges, generate spectra corresponding to
             the requested vsini and resolving power.

             INPUT:
                 vsini - rotational broadening - km/s
                 R - resolving power

             OUTPUT:
                 none

        The 
        '''
        for melody in self.melodies:
            if not(melody.muted):
                melody.rehearse(vsini=vsini, R=R)

    def perform(self, vsini = 0.0, R = 0.0):
        spectra = []
        labels = []
        for melody in self.melodies:
            if not(melody.muted):
                sp, label = melody.perform(vsini=vsini, R=R)
                spectra.append(sp)
                labels.append(label)

        return spectra, labels

    def record(self, outfilename):
        for melody in self.melodies:
            if not(melody.muted):
                melody.record(outfilename)

    """
    def __init__(self, datafile, ID, resolvingPower):
        self.datafile = datafile
        self.ID = ID
        self.resolvingPower = resolvingPower
        info = pyfits.info(self.datafile, output='')
        self.nSpectra = len(info)-1
        wavestart = []
        wavestop = []
        self.headers = []
        for i in range(self.nSpectra):
            self.headers.append(pyfits.getheader(self.datafile, ext=i+1))
            wavestart.append(self.headers[-1].get('WLSTART'))
            wavestop.append(self.headers[-1].get('WLSTOP'))

        self.wavestart = numpy.array(wavestart)
        self.wavestop = numpy.array(wavestop)
        header = pyfits.getheader(self.datafile)
        self.Teff = header.get("TEFF")
        self.logg = header.get("LOGG")
        self.B = header.get("BFIELD")
        self.vsini = header.get("VSINI")
        self.generate_label()
        self.suppressed = True

    def generate_label(self):
        self.label = "T%4d G%.1f B%.1f V%.1f" % (self.Teff, self.logg, self.B, self.vsini)

    def print_info(self):
        if self.suppressed:
            print("#%d)  %s" % (self.ID, self.label))
        else:
            print("#%d)* %s" % (self.ID, self.label))

    def play(self):
        if self.suppressed:
            return None
        else:
            waves = []
            fluxes = []
            self.loadSpectra()
            # now look for overlaps
            for w, f in zip(self.wave[self.inWlRange==True], self.flux[self.inWlRange==True]):
                waves.append(w)
                fluxes.append(f)
            overlaps = numpy.intersect1d(self.wavestart[self.inWlRange==True], self.wavestop[self.inWlRange==True])
            blue_indices = []
            red_indices = []
            stitched_waves = []
            stitched_fluxes = []
            for overlap in overlaps:
                blue_index = self.wavestop[self.inWlRange==True] == overlap
                red_index = self.wavestart[self.inWlRange==True] == overlap

                for b in numpy.arange(self.nWithinRange)[blue_index]:

                    for r in numpy.arange(self.nWithinRange)[red_index]:
                        stitched_waves.append(numpy.append(waves[b][:-1], waves[r]))
                        stitched_fluxes.append(numpy.append(fluxes[b][:-1], fluxes[r]))
                        if len(blue_indices) == 0:
                            red_indices.append(r)
                    blue_indices.append(b)
            new_waves = []
            new_fluxes = []
            for i in range(self.nWithinRange):
                if not(i in red_indices) and (not(i in blue_indices)):
                    new_waves.append(waves[i])
                    new_fluxes.append(fluxes[i])
            for i in range(len(stitched_waves)):
                new_waves.append(stitched_waves[i])
                new_fluxes.append(stitched_fluxes[i])
            return (self.label, new_waves, new_fluxes)

    def __eq__(self, other):
        try:
            return int(other) == self.ID
        except:
            return self.datafile == other

    def inWlRange(self, wlStart, wlStop):
        inWlRange = []
        for wavestart, wavestop in zip(self.wavestart, self.wavestop):
            if (wavestart < wlStop) & (wavestop > wlStart):
                inWlRange.append(True)
            else:
                inWlRange.append(False)
        self.inWlRange = numpy.array(inWlRange)
        self.nWithinRange = numpy.sum(self.inWlRange)
        if any(self.inWlRange):
            return True
        else:
            return False

    def loadSpectra(self):
        self.wave = []
        self.flux = []
        for i, good in zip(range(self.nSpectra), self.inWlRange):
            if good:
                data = pyfits.getdata(self.datafile, ext=i+1)
                if self.resolvingPower != None:
                    wave, flux = SpectralTools.resample(data.field('Wavelength'), 
                        data.field('Stokes_I'), self.resolvingPower)
                    self.wave.append(wave)
                    self.flux.append(flux)
                else:
                    self.wave.append(data.field('Wavelength'))
                    self.flux.append(data.field('Stokes_I'))
            else:
                self.wave.append([])
                self.flux.append([])
        #self.wave, self.flux = SpectralTools.resample(data[0], data[1], 
        #        self.resolvingPower)
        self.wave = numpy.array(self.wave)
        self.flux = numpy.array(self.flux)
        #"""

class Moog960( object ):
    def __init__(self, configFile):
        self.config = AstroUtils.parse_config(configFile)
        self.applyConfigFile()

    def applyConfigFile(self):
        self.watchedDir = self.config["watched_dir"]
        self.wlRange = numpy.array(self.config["wlRange"].split(), dtype=numpy.int)
        keys = self.config.keys()
        if "TeffRange" in keys:
            self.TeffRange = numpy.array(self.config["TeffRange"].split(),
                    dtype=numpy.int)
        else:
            self.TeffRange = numpy.array([0, 100000])
        if "loggRange" in keys:
            self.loggRange = numpy.array(self.config["loggRange"].split(),
                    dtype=numpy.float32)
        else:
            self.loggRange = numpy.array([2.5, 6.0])
        if "BfieldRange" in keys:
            self.BfieldRange = numpy.array(self.config["BfieldRange"].split(),
                    dtype=numpy.float32)
        else:
            self.BfieldRange = numpy.array([0.0, 20.0])
        self.resolvingPower = self.config["resolving_power"]
        if 'vsini' in keys:
            self.vsini = self.config['vsini']
        else:
            self.vsini = None
        self.Score = Score(directory=self.watchedDir)
        self.Score.selectMelodies(TeffRange=self.TeffRange, loggRange=self.loggRange,
                BfieldRange=self.BfieldRange, wlRange=self.wlRange)
        #, vsini=self.vsini,
        #        R=self.resolvingPower)
        #self.Score.setWlRange(self.wlStart, self.wlStop)

    def rehearse(self, vsini = None, R = None):
        if vsini == None:
            vsini = [self.vsini]
        if R == None:
            R = [self.resolvingPower]
        for v, r in zip(vsini, R):
            self.Score.rehearse(vsini=v, R=r)

    def perform(self, vsini=None, R = None, axes= None):

        if vsini == None:
            vsini = [self.vsini]
        if R == None:
            R = [self.resolvingPower]
        
        spectra = []
        labels = []
        for v, r in zip(vsini, R):
            sp, l = self.Score.perform(vsini=v, R = r)
            spectra.append(sp[0])
            labels.append(l[0])
        for sp, l in zip(spectra,labels):
            for s in sp:
                line = axes.plot(s.wl, s.flux_I, label=l)

        #axes.figure.legend(lines, labels)


    def loadMelodies(self):
        spectra = glob.glob(self.watchedDir+'*.fits')
        for spectrum in spectra:
            if not(spectrum in self.Score.melodies):
                track = Player(spectrum, len(self.tracks), self.resolvingPower)
                if track.inWlRange(self.wlStart, self.wlStop):
                    self.tracks.append(tracks)

    def selectTracks(self):
        self.getTracks()
        for spectrum in self.tracks:
            spectrum.print_info()

        selection = raw_input("Enter space-separated list of spectra to Toggle :").split()

        for source in selection:
            for spectrum in self.tracks:
                if spectrum == source:
                    spectrum.suppressed = not(spectrum.suppressed)


    def getEnsemble(self):
        spectra = []
        labels = []
        for player in self.players:
            if not(player.suppressed):
                label, wave, flux = player.play()
                labels.append(label)
                spectra.append([wave, flux])

        return spectra, labels
