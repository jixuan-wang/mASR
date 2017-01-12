from ipapy.arpabetmapper import ARPABETMapper
import re
import sys

'''
This program transforms IPA to Arpabet using ipapy.
The IPA format is got from Oxford online dictionary.
Sometimes, by searching a single word, like 'abruptio', a set of words will be returned as results, in this case, the results are 'abruptio placentae'. In this case, you should decide the pronounciation of your target word mannually. Words like this will be marked with 'FIX ME'

'''

amapper = ARPABETMapper()

if __name__ == "__main__":
    if len(sys.argv) == 3:
        fn = sys.argv[1]
        oname = sys.argv[2]

        ofile = open(oname, 'w')

        for line in open(fn, 'r'):
            temp = line.strip().split('\t')

            multi_words = False
            word = temp[0]
            prons = set()
            print word
            for tp in temp[1:]:
                tp = tp[1:-1] # elimate /
                if re.search(r' ', tp):
                    multi_words = True
                if re.search(r'\(.*\)', tp): # contains '()' means multiple prons
                    t = re.sub(r'\(|\)', '', tp)
                    prons.add(' '.join(amapper.map_unicode_string(t.decode('utf-8'), ignore=True, return_as_list=True)))

                    t = re.sub(r'\(.*\)', '', tp)
                    prons.add(' '.join(amapper.map_unicode_string(t.decode('utf-8'), ignore=True, return_as_list=True)))
                else:
                    prons.add(' '.join(amapper.map_unicode_string(tp.decode('utf-8'), ignore=True, return_as_list=True)))

            if len(prons) > 0:
                if multi_words:
                    ofile.write('[FIX ME]')
                ofile.write(word + '\t' + prons.pop() + '\n')
                i = 1
                if len(prons) > 0:
                    for p in prons:
                        ofile.write(word + '('+str(i)+')\t' + p + '\n')
                        i += 1
    ofile.close()
                        

                    





                

            


