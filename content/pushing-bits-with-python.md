Title: Pushing Bits with Python
Date: 2016-06-17
Author: Chris
Slug: pushing-bits-with-python
Category: code & tutorials
Status: Published

When was the last time you needed to directly manipulate a bunch of
binary data? Most engineers run
across it only in the context of bit flags and masks in C++ or Java.

It's a little rarer to muck about with direct binary file
data. It's nonetheless quite a bit of fun, and a good party
trick<sup>[1](#footnote1)</sup>. And, how are you going to solve the
next [Cicada 3301](https://en.wikipedia.org/wiki/Cicada_3301) puzzle
without being able to XOR together a bunch of Tor Onion addresses with
[mysterious audio signals](http://uncovering-cicada.wikia.com/wiki/XOR_all_the_things)<sup>[2](#footnote2)</sup>?

If you want to learn, then good news -- Python has you covered! The
awesome [bitstring](http://pythonhosted.org/bitstring/) module makes
it simple to take raw data in whatever form you have it (bits, hex,
octal, a file stream) and inspect or manipulate it. Be sure to ``pip
install bitstring`` to follow along. Away we go!

## Create a BitArray from scratch

To start, let's use bitstring to create a raw 12-bit binary object,
and initialize it to 256. Then we'll take a look at the object in a
bunch of different raw formats.

    :::python
    from bitstring import *

    twofiftysix = BitArray(uint=256, length=12)

Note that we specified the length of the BitArray so that we have
enough bits to convert to Hex and Octal. If we just took 256 as
100000000, then we can't display a corresponding Hex string because
each Hex character represents 4 bits, and 256 in binary is only 9 bits
long. By specifying a length of 12, our BitArray is padded with 3
leading 0s, and we can convert cleanly into Hex and Octal.

Show me the money!

    :::python
    print "Int: %s, Binary: %s, Hex: %s, Oct: %s" %
        (twofiftysix.uint, twofiftysix.bin, twofiftysix.hex, twofiftysix.oct)

    > 'Int: 256, Binary: 000100000000, Hex: 100, Oct: 0400'

## Manipulation

We can manipulate the bits directly as well. Here we'll create a
couple of BitArrays, and XOR them together. Bitstring overrides the ^
operator to perform an XOR.

    :::python
    bits1 = BitArray(hex='2ba49fe')
    bits2 = BitArray(hex='f55e513')

    print bits1.bin
    print bits2.bin
    print "                    XOR'ed ="
    print (bits1 ^ bits2).bin
    print "\nAnd in hex:"
    print (bits1 ^ bits2).bin + " = '" + (bits1 ^ bits2).hex + "'"

Results:

    0010101110100100100111111110
    1111010101011110010100010011
                        XOR'ed =
    1101111011111010110011101101

    In hex:
    1101111011111010110011101101 = 'defaced'

Did you know 'defaced' is the longest english word you can spell with
just ABCDEF!  Another awesome fact for your cocktail party banter.

## File type detection

Here's something a little more practical. Let's say we have
[4 images]({static}files/mystery-images.zip), with no file
extensions, called mystery1, mystery2, mystery3, and mystery4. Some
quick Googling will tell us the leading bits of some common image
types. We can load up the images, inspect the first bits, and figure
out the file type.

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


### Notes

<a name="footnote1">1</a>: If this does not impress, you are obviously
going to the wrong sorts of parties.

<a name="footnote2">2</a>: For what it's worth, this is literally the
reason the learned how to do this in the first place. Is that
embarassing, or cool? I guess it depends what kind of party you're at.
