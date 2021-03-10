# These functions written by Ryan Anderson (rbanderson@usgs.gov), March 10, 2021.
# Adapted from SuperCam-specific scripts to be more generic.

from skimage import io
import numpy as np
import scipy.interpolate as interp
import matplotlib.pyplot as plot

def get_color_lookup(input_wvls):
    #load the image
    spect_img_path = "Linear_visible_spectrum.png"
    spect_img = io.imread(spect_img_path)

    #take a slice of the image, containing just the colors (no margins, etc)
    spect_colors = spect_img[200,7:1909,0:3]/255

    #create an array with values corresponding to the wavelength scale on the image
    wvl_range = (750.0-380.0)
    spect_wvls = np.array(list(range(spect_colors.shape[0])))/spect_colors.shape[0]*wvl_range+380

    #for each color (R,G,B) interpolate the values from the spectrum image onto the input wavelengths
    #(for values outside the spectrum image range, use black)
    f_red = interp.interp1d(spect_wvls, spect_colors[:, 0], bounds_error=False, fill_value=0)
    f_green = interp.interp1d(spect_wvls, spect_colors[:, 1], bounds_error=False, fill_value=0)
    f_blue = interp.interp1d(spect_wvls, spect_colors[:, 2], bounds_error=False, fill_value=0)

    input_red = f_red(input_wvls)
    input_green = f_green(input_wvls)
    input_blue = f_blue(input_wvls)

    #return the rgb values for each input wvl
    return np.vstack((input_red, input_green, input_blue)).T

def color_lineplot(ax, x,y,colors):
    # plot the spectrum segment by segment, using the specified colors
    # (This assumes that the segments are small compared to the change in color over the spectrum.
    # Could look weird for low spectral resolution.)
    for i in range(len(x)):
        try:
            ax.plot(x[i:i+2],y[i:i+2], color = colors[i], linewidth = 1, solid_capstyle= 'round')
        except:
            pass

########## Example #########

#make a fake wvl array and matching fake data (substitute real data here)
wvls = np.arange(200,900,0.1)
fake_spect = np.sin(wvls/np.pi)

#look up rgb colors matching each wvl
color_values = get_color_lookup(wvls)

#get indices for three spectral ranges
range1_ind = np.all((wvls > 240, wvls < 340), axis=0)
range2_ind = np.all((wvls > 379, wvls < 465), axis=0)
range3_ind = np.all((wvls > 535, wvls < 855), axis=0)

fig, (ax1, ax2, ax3) = plot.subplots(1, 3, figsize=(10,4))
# plot color coded lines
color_lineplot(ax1, wvls[range1_ind], fake_spect[range1_ind], color_values[range1_ind])
color_lineplot(ax2, wvls[range2_ind], fake_spect[range2_ind], color_values[range2_ind])
color_lineplot(ax3, wvls[range3_ind], fake_spect[range3_ind], color_values[range3_ind])

# narrow plot spacing
plot.subplots_adjust(wspace=0.01)

# remove yticks
ax1.set_yticks([])
ax2.set_yticks([])
ax3.set_yticks([])

# labels
ax1.set_ylabel('Y Axis Title')
ax2.set_xlabel('X Axis Title')

# titles
fig.suptitle('Example colorized spectrum')
ax1.set_title('Range 1')
ax2.set_title('Range 2')
ax3.set_title('Range 3')

# plot.show()
dpi = 1000
plot.savefig('example_fig_' + str(dpi) + 'dpi.png', dpi=dpi)
