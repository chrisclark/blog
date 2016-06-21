Title: Pushing Bits with Python
Date: 2016-06-17
Author: Chris
Slug: pushing-bits-with-python
Category: code & tutorials

Ever wanted to directly manipulate binary data? Perhaps not, given that it's somewhat of a specialty need, but should that need arise, Python has you covered! The awesome [bitstring](http://pythonhosted.org/bitstring/) module makes it super simple take raw data in whatever form you have it (bits, hex, octal, a file) and manipulate the raw bits. Be sure to ``pip install bitstring``. Away we go!

## Create a BitArray from scratch

    :::python
    from bitstring import *

    # Create a Bit Array with 12 digits, and intialize it to 256.
    # e.g 000100000000
    twofiftysix = BitArray(uint=256, length=12)
    print "Int: %s, Binary: %s, Hex: %s, Oct: %s" % (twofiftysix.uint, twofiftysix.bin, twofiftysix.hex, twofiftysix.oct)

And we get:

    > Int: 256, Binary: 000100000000, Hex: 100, Oct: 0400

## Manipulation

We can manipulate the bits directly as well. Here we'll create a couple of BitArrays, and XOR them together. Bitstring overrides the ^ operator to perform an XOR.

    :::python
    bits1 = BitArray(hex='2ba49fe')
    bits2 = BitArray(hex='f55e513')

    print bits1.bin
    print bits2.bin
    print "--------------------- XOR'ed"
    print (bits1 ^ bits2).bin
    print "\nAnd in hex:"
    print (bits1 ^ bits2).bin + " = '" + (bits1 ^ bits2).hex + "'"

Results:

    0010101110100100100111111110
    1111010101011110010100010011
    --------------------- XOR'ed
    1101111011111010110011101101
    
    In hex:
    1101111011111010110011101101 = 'defaced'

That's the longest english word you can spell with just ABCDEF! With that fact in your back pocket, you'll be a hit at every cocktail party.

## File type detection

Now let's try something a little more practical. Let's say we have [4 images]({filename}/files/mystery-images.zip), with no file extensions, called mystery1, mystery2, and mystery3. Some quick Googling will tell us what bits some common image types are expected to start with, so we can load up the images, inspect the first bits, and find what image file type they match.

    :::python
    types = {
        'bmp': '424d',  # Converted to ASCII, this is 'BM'
        'gif': '474946',  # Converted to ASCII, this is 'GIF'
        'jpeg': 'ffd8ff',
        'png': "89504e470d0a1a0a"
    }
    
    images = [
        'mystery1',
        'mystery2',
        'mystery3',
        'mystery4'
    ]
    
    def detect(name, bits):
        for img_type, pattern in types.items():
            try:
                if bits.hex.index(pattern) == 0:
                    print "%s is %s (first bits were %s)" % (name, img_type, bits.hex[:8])
                    return
            except:
                continue
        print "Could not identify %s. First bits: %s" % (name, bits.hex[:4])
    
    for i in images:
        with open(i, 'r') as f:
            img = Bits(f)
            detect(i, img)

Problem solved!

    mystery1 is jpeg (first bits were ffd8ffe1)
    mystery2 is gif (first bits were 47494638)
    mystery3 is png (first bits were 89504e47)
    mystery4 is bmp (first bits were 424d0072)

## Converting to & from ASCII

One last trick; using the built-in binascii library, we can convert ascii to bits and back.

    :::python
    # The built-in binascii library can convert binary to bits
    hex = binascii.hexlify('foobar')
    bits = BitArray(hex=hex)
    print bits.bin

We get:

    011001100110111101101111011000100110000101110010

...which we can then convert back to an ASCII string:

    :::python
    print binascii.unhexlify(bits.hex)
    > foobar
