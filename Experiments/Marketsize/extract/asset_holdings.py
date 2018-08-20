
import numpy as np
import pandas as pd

def extract_domestic_agent_assets(key_dict,  d_dc_dict_assets, d_fc_dict_assets , d_da_dict_assets , d_fa_dict_assets):
	# For assets
	D_DC_assets_mean = np.empty((0,2), float)
	D_DC_assets_5 =np.empty((0,2), float)
	D_DC_assets_95 =np.empty((0,2), float)

	D_FC_assets_mean = np.empty((0,2), float)
	D_FC_assets_5 =np.empty((0,2), float)
	D_FC_assets_95 =np.empty((0,2), float)

	D_DA_assets_mean = np.empty((0,2), float)
	D_DA_assets_5 =np.empty((0,2), float)
	D_DA_assets_95 =np.empty((0,2), float)

	D_FA_assets_mean = np.empty((0,2), float)
	D_FA_assets_5 =np.empty((0,2), float)
	D_FA_assets_95 =np.empty((0,2), float)

	for i in sorted(key_dict.iterkeys()):
		f = np.array(key_dict[i])
		D_DC_assets_mean = np.append(D_DC_assets_mean,np.array([[float(i.split("_")[-1]), np.mean(np.array(d_dc_dict_assets[i]))]]), axis=0)
		D_FC_assets_mean = np.append(D_FC_assets_mean, np.array([[float(i.split("_")[-1]), np.mean(np.array(d_fc_dict_assets[i]))]]), axis=0)
		D_DA_assets_mean = np.append(D_DA_assets_mean, np.array([[float(i.split("_")[-1]), np.mean(np.array(d_da_dict_assets[i]))]]), axis=0)
		D_FA_assets_mean = np.append(D_FA_assets_mean, np.array([[float(i.split("_")[-1]), np.mean(np.array(d_fa_dict_assets[i]))]]), axis=0)

		D_DC_assets_5 = np.append(D_DC_assets_5, np.array([[float(i.split("_")[-1]), np.percentile(np.array(d_dc_dict_assets[i]), 5)]]), axis=0)

		D_FC_assets_5 = np.append(D_FC_assets_5, np.array([[float(i.split("_")[-1]), np.percentile(np.array(d_fc_dict_assets[i]), 5)]]), axis=0)

		D_DA_assets_5 = np.append(D_DA_assets_5, np.array([[float(i.split("_")[-1]), np.percentile(np.array(d_da_dict_assets[i]), 5)]]), axis=0)

		D_FA_assets_5 = np.append(D_FA_assets_5, np.array([[float(i.split("_")[-1]), np.percentile(np.array(d_fa_dict_assets[i]), 5)]]), axis=0)

		D_DC_assets_95 = np.append(D_DC_assets_95, np.array([[float(i.split("_")[-1]), np.percentile(np.array(d_dc_dict_assets[i]), 95)]]), axis=0)

		D_FC_assets_95 = np.append(D_FC_assets_95, np.array([[float(i.split("_")[-1]), np.percentile(np.array(d_fc_dict_assets[i]), 95)]]), axis=0)

		D_DA_assets_95 = np.append(D_DA_assets_95, np.array([[float(i.split("_")[-1]), np.percentile(np.array(d_da_dict_assets[i]), 95)]]), axis=0)

		D_FA_assets_95 = np.append(D_FA_assets_95, np.array([[float(i.split("_")[-1]), np.percentile(np.array(d_fa_dict_assets[i]), 95)]]), axis=0)



	return D_DA_assets_mean, D_DA_assets_5, D_DA_assets_95,\
	       D_DC_assets_mean,  D_DC_assets_5, D_DC_assets_95, \
	       D_FA_assets_mean,   D_FA_assets_5, D_FA_assets_95, \
	       D_FC_assets_mean,  D_FC_assets_5, D_FC_assets_95


def extract_domestic_agent_weights(key_dict,  d_dc_dict_weights, d_fc_dict_weights , d_da_dict_weights , d_fa_dict_weights):
	# For assets
	D_DC_mean = np.empty((0,2), float)
	D_DC_5 =np.empty((0,2), float)
	D_DC_95 =np.empty((0,2), float)

	D_FC_mean = np.empty((0,2), float)
	D_FC_5 =np.empty((0,2), float)
	D_FC_95 =np.empty((0,2), float)

	D_DA_mean = np.empty((0,2), float)
	D_DA_5 =np.empty((0,2), float)
	D_DA_95 =np.empty((0,2), float)

	D_FA_mean = np.empty((0,2), float)
	D_FA_5 =np.empty((0,2), float)
	D_FA_95 =np.empty((0,2), float)

	for i in sorted(key_dict.iterkeys()):
		f = np.array(key_dict[i])
		D_DC_mean = np.append(D_DC_mean,np.array([[float(i.split("_")[-1]), np.mean(np.array(d_dc_dict_weights[i]))]]), axis=0)
		D_FC_mean = np.append(D_FC_mean, np.array([[float(i.split("_")[-1]), np.mean(np.array(d_fc_dict_weights[i]))]]), axis=0)
		D_DA_mean = np.append(D_DA_mean, np.array([[float(i.split("_")[-1]), np.mean(np.array(d_da_dict_weights[i]))]]), axis=0)
		D_FA_mean = np.append(D_FA_mean, np.array([[float(i.split("_")[-1]), np.mean(np.array(d_fa_dict_weights[i]))]]), axis=0)

		D_DC_5 = np.append(D_DC_5, np.array([[float(i.split("_")[-1]), np.percentile(np.array(d_dc_dict_weights[i]), 5)]]), axis=0)

		D_FC_5 = np.append(D_FC_5, np.array([[float(i.split("_")[-1]), np.percentile(np.array(d_fc_dict_weights[i]), 5)]]), axis=0)

		D_DA_5 = np.append(D_DA_5, np.array([[float(i.split("_")[-1]), np.percentile(np.array(d_da_dict_weights[i]), 5)]]), axis=0)

		D_FA_5 = np.append(D_FA_5, np.array([[float(i.split("_")[-1]), np.percentile(np.array(d_fa_dict_weights[i]), 5)]]), axis=0)

		D_DC_95 = np.append(D_DC_95, np.array([[float(i.split("_")[-1]), np.percentile(np.array(d_dc_dict_weights[i]), 95)]]), axis=0)

		D_FC_95 = np.append(D_FC_95, np.array([[float(i.split("_")[-1]), np.percentile(np.array(d_fc_dict_weights[i]), 95)]]), axis=0)

		D_DA_95 = np.append(D_DA_95, np.array([[float(i.split("_")[-1]), np.percentile(np.array(d_da_dict_weights[i]), 95)]]), axis=0)

		D_FA_95 = np.append(D_FA_95, np.array([[float(i.split("_")[-1]), np.percentile(np.array(d_fa_dict_weights[i]), 95)]]), axis=0)



	return D_DA_mean, D_DA_5, D_DA_95,\
	       D_DC_mean,  D_DC_5, D_DC_95, \
	       D_FA_mean,   D_FA_5, D_FA_95, \
	       D_FC_mean,  D_FC_5, D_FC_95


def extract_domestic_agent_assets(key_dict,  f_dc_dict_assets, f_fc_dict_assets , f_da_dict_assets , f_fa_dict_assets):
	# For assets
	F_DC_assets_mean = np.empty((0,2), float)
	F_DC_assets_5 =np.empty((0,2), float)
	F_DC_assets_95 =np.empty((0,2), float)

	F_FC_assets_mean = np.empty((0,2), float)
	F_FC_assets_5 =np.empty((0,2), float)
	F_FC_assets_95 =np.empty((0,2), float)

	F_DA_assets_mean = np.empty((0,2), float)
	F_DA_assets_5 =np.empty((0,2), float)
	F_DA_assets_95 =np.empty((0,2), float)

	F_FA_assets_mean = np.empty((0,2), float)
	F_FA_assets_5 =np.empty((0,2), float)
	F_FA_assets_95 =np.empty((0,2), float)

	for i in sorted(key_dict.iterkeys()):
		f = np.array(key_dict[i])
		F_DC_assets_mean = np.append(F_DC_assets_mean,np.array([[float(i.split("_")[-1]), np.mean(np.array(f_dc_dict_assets[i]))]]), axis=0)
		F_FC_assets_mean = np.append(F_FC_assets_mean, np.array([[float(i.split("_")[-1]), np.mean(np.array(f_fc_dict_assets[i]))]]), axis=0)
		F_DA_assets_mean = np.append(F_DA_assets_mean, np.array([[float(i.split("_")[-1]), np.mean(np.array(f_da_dict_assets[i]))]]), axis=0)
		F_FA_assets_mean = np.append(F_FA_assets_mean, np.array([[float(i.split("_")[-1]), np.mean(np.array(f_fa_dict_assets[i]))]]), axis=0)

		F_DC_assets_5 = np.append(F_DC_assets_5, np.array([[float(i.split("_")[-1]), np.percentile(np.array(f_dc_dict_assets[i]), 5)]]), axis=0)

		F_FC_assets_5 = np.append(F_FC_assets_5, np.array([[float(i.split("_")[-1]), np.percentile(np.array(f_fc_dict_assets[i]), 5)]]), axis=0)

		F_DA_assets_5 = np.append(F_DA_assets_5, np.array([[float(i.split("_")[-1]), np.percentile(np.array(f_da_dict_assets[i]), 5)]]), axis=0)

		F_FA_assets_5 = np.append(F_FA_assets_5, np.array([[float(i.split("_")[-1]), np.percentile(np.array(f_fa_dict_assets[i]), 5)]]), axis=0)

		F_DC_assets_95 = np.append(F_DC_assets_95, np.array([[float(i.split("_")[-1]), np.percentile(np.array(f_dc_dict_assets[i]), 95)]]), axis=0)

		F_FC_assets_95 = np.append(F_FC_assets_95, np.array([[float(i.split("_")[-1]), np.percentile(np.array(f_fc_dict_assets[i]), 95)]]), axis=0)

		F_DA_assets_95 = np.append(F_DA_assets_95, np.array([[float(i.split("_")[-1]), np.percentile(np.array(f_da_dict_assets[i]), 95)]]), axis=0)

		F_FA_assets_95 = np.append(F_FA_assets_95, np.array([[float(i.split("_")[-1]), np.percentile(np.array(f_fa_dict_assets[i]), 95)]]), axis=0)



	return F_DA_assets_mean, F_DA_assets_5, F_DA_assets_95,\
	       F_DC_assets_mean,  F_DC_assets_5, F_DC_assets_95, \
	       F_FA_assets_mean,   F_FA_assets_5, F_FA_assets_95, \
	       F_FC_assets_mean,  F_FC_assets_5, F_FC_assets_95


def extract_foreign_agent_weights(key_dict,  f_dc_dict_weights, f_fc_dict_weights , f_da_dict_weights , f_fa_dict_weights):
	# For assets
	F_DC_mean = np.empty((0,2), float)
	F_DC_5 =np.empty((0,2), float)
	F_DC_95 =np.empty((0,2), float)

	F_FC_mean = np.empty((0,2), float)
	F_FC_5 =np.empty((0,2), float)
	F_FC_95 =np.empty((0,2), float)

	F_DA_mean = np.empty((0,2), float)
	F_DA_5 =np.empty((0,2), float)
	F_DA_95 =np.empty((0,2), float)

	F_FA_mean = np.empty((0,2), float)
	F_FA_5 =np.empty((0,2), float)
	F_FA_95 =np.empty((0,2), float)

	for i in sorted(key_dict.iterkeys()):
		f = np.array(key_dict[i])
		F_DC_mean = np.append(F_DC_mean,np.array([[float(i.split("_")[-1]), np.mean(np.array(f_dc_dict_weights[i]))]]), axis=0)
		F_FC_mean = np.append(F_FC_mean, np.array([[float(i.split("_")[-1]), np.mean(np.array(f_fc_dict_weights[i]))]]), axis=0)
		F_DA_mean = np.append(F_DA_mean, np.array([[float(i.split("_")[-1]), np.mean(np.array(f_da_dict_weights[i]))]]), axis=0)
		F_FA_mean = np.append(F_FA_mean, np.array([[float(i.split("_")[-1]), np.mean(np.array(f_fa_dict_weights[i]))]]), axis=0)

		F_DC_5 = np.append(F_DC_5, np.array([[float(i.split("_")[-1]), np.percentile(np.array(f_dc_dict_weights[i]), 5)]]), axis=0)

		F_FC_5 = np.append(F_FC_5, np.array([[float(i.split("_")[-1]), np.percentile(np.array(f_fc_dict_weights[i]), 5)]]), axis=0)

		F_DA_5 = np.append(F_DA_5, np.array([[float(i.split("_")[-1]), np.percentile(np.array(f_da_dict_weights[i]), 5)]]), axis=0)

		F_FA_5 = np.append(F_FA_5, np.array([[float(i.split("_")[-1]), np.percentile(np.array(f_fa_dict_weights[i]), 5)]]), axis=0)

		F_DC_95 = np.append(F_DC_95, np.array([[float(i.split("_")[-1]), np.percentile(np.array(f_dc_dict_weights[i]), 95)]]), axis=0)

		F_FC_95 = np.append(F_FC_95, np.array([[float(i.split("_")[-1]), np.percentile(np.array(f_fc_dict_weights[i]), 95)]]), axis=0)

		F_DA_95 = np.append(F_DA_95, np.array([[float(i.split("_")[-1]), np.percentile(np.array(f_da_dict_weights[i]), 95)]]), axis=0)

		F_FA_95 = np.append(F_FA_95, np.array([[float(i.split("_")[-1]), np.percentile(np.array(f_fa_dict_weights[i]), 95)]]), axis=0)



	return F_DA_mean, F_DA_5, F_DA_95,\
	       F_DC_mean,  F_DC_5, F_DC_95, \
	       F_FA_mean,   F_FA_5, F_FA_95, \
	       F_FC_mean,  F_FC_5, F_FC_95