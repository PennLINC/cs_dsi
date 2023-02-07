import shutil
import nibabel as nb
import numpy as np
from dipy.segment.mask import median_otsu
from dipy.core.gradients import gradient_table
from brainsuite_shore import BrainSuiteShoreModel, brainsuite_shore_basis #direct download from github
import os
import sys
from dipy.io.image import load_nifti
from dipy.io import read_bvals_bvecs
import numpy as np
from dipy.core.gradients import gradient_table


def get_mask(dwi_data, gtab, affine, header):
    _, mask_array = median_otsu(dwi_data,
                                vol_idx=gtab.b0s_mask,
                                median_radius=3,
                                numpass=2)

    # Needed for synthetic data
    mask_array = mask_array * (dwi_data.sum(3) > 0)
    mask_img = nb.Nifti1Image(mask_array.astype(np.float32), affine,
                              header)
    return mask_array, mask_img

def get_model_fit(data, gtab):
    odfmodel = BrainSuiteShoreModel(gtab, radial_order = 8, regularization='L2')
    # ^^ CZ: param confirmed;
    odffit = odfmodel.fit(data)
    return odffit


def extrapolate_scheme(fit_obj, odir, acq, mask_array, mask_img):
    output_dwi_file = odir+"acq-"+acq+"_dsi_extrapolated.nii.gz"
    output_bval_file = odir+"acq-"+acq+"_dsi_extrapolated.bval"
    output_bvec_file = odir+"acq-"+acq+"_dsi_extrapolated.bvec"


    # Copy in the bval and bvecs
    bval_file = "/cbica/projects/csdsi/BIDS/qsiprep_unzipped/full_dsi.bval" #pass in full DSI scheme
    bvec_file = "/cbica/projects/csdsi/BIDS/qsiprep_unzipped/full_dsi.bvec"
    shutil.copyfile(bval_file, output_bval_file)   # CZ: predicted bval, i.e., full DSI scheme
    shutil.copyfile(bvec_file, output_bvec_file)

    # Get prediction from odf fit:
    prediction_gtab = gradient_table(bvals=np.loadtxt(bval_file), bvecs=np.loadtxt(bvec_file).T, b0_threshold=10, big_delta=0.04684, small_delta=0.0305) 
    # ^^ CZ: bvals and bvects to be predicted, in a full DSI scheme
    prediction_shore = brainsuite_shore_basis(fit_obj.model.radial_order, fit_obj.model.zeta,
                                              prediction_gtab, fit_obj.model.tau)

    # Fill in mask with extrapolated signal.
    shore_array = fit_obj._shore_coef[mask_array]
    output_data = np.zeros(mask_array.shape + (len(prediction_gtab.bvals),))
    output_data[mask_array] = np.dot(shore_array, prediction_shore.T)

    nb.save(nb.Nifti1Image(output_data, mask_img.affine, mask_img.header), output_dwi_file)
    # ^^ CZ: the `mask_img.header` has been set to use original dwi's header, in `get_mask()`
        
def run_extrapolate_scheme(indir, sub, acq, odir):
    # Load data:
    nii_file = indir+"sub-"+sub+"_ses-1_acq-"+acq+"_space-T1w_desc-preproc_dwi.nii.gz"
    bval_file = indir+"sub-"+sub+"_ses-1_acq-"+acq+"_space-T1w_desc-preproc_dwi.bval"
    bvec_file = indir+"sub-"+sub+"_ses-1_acq-"+acq+"_space-T1w_desc-preproc_dwi.bvec"
    data, affine = load_nifti(nii_file)
    bvals, bvecs = read_bvals_bvecs(bval_file, bvec_file)
    gtab = gradient_table(bvals, bvecs, b0_threshold=10, big_delta=0.04684, small_delta=0.0305) 

    # Fit odf:
    odffit = get_model_fit(data, gtab)
    mask_array, mask_img = get_mask(data, gtab, affine, nb.load(nii_file).header)   
    if os.path.exists(odir) == False:
        os.makedirs(odir)

    # Extrapolate DSI
    extrapolate_scheme(odffit, odir, acq, mask_array, mask_img)

sub = sys.argv[1]
acq = sys.argv[2]
indir = sys.argv[3]
odir = sys.argv[4]
run_extrapolate_scheme(indir, sub, acq, odir)

# # Example variables:
# CZ: `indir` below is for prosp dataset but sub IDs are retro. So just use prosp subject ID.
# sub in 0001a 1041h 1665h 2211h 3058s 4558a 4936m 0097p 1043f 1808u 2453z 3571z 4662a 4961a 0444g 1142k 1853b 2741x 3832y 4680i 0798q 1145h 2027j 2755j 3992u 4917f
# acq in HASC92 HASC55_run-01 HASC55_run-02 RAND57 HASC92-55_run-01 HASC92-55_run-02
# indir = "/cbica/projects/csdsi/BIDS/qsiprep_unzipped/sub-"+sub+"/ses-1/dwi/"
# odir = "/cbica/projects/csdsi/BIDS/derivatives/extrapolated/sub-"+sub+"/" # please edit so that you don't rewrite

