
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def main():
    # read senti in
    df_senti = pd.read_csv('senti_all.txt', sep=' ', header=None)
    senti = np.array([df_senti[1].values, df_senti[2].values, df_senti[3].values]).T
    senti_valid = []
    for i in range(len(senti)):
        if np.amin(senti[i]) == -1:
            senti_valid.append(False)
        else:
            senti_valid.append(True)
    senti_valid = np.array(senti_valid)
    senti_mean = np.mean(senti, axis=1)
    senti_median = np.median(senti, axis=1)
    senti_max = np.amax(senti, axis=1)
    senti_min = np.amin(senti, axis=1)
    senti_std = np.std(senti, axis=1)
    senti_feat = np.array([senti_mean, senti_median, senti_max, senti_min, senti_std]).T

    senti_all = np.concatenate((senti, senti_feat), axis=1)
    feature_names = ['risk', 'discussion', 'market_risk', 'mean', \
                    'median', 'max', 'min', 'std']

    # read company
    df_com = pd.read_csv('out.csv')
    sector = df_com['sector'].values
    sector = sector[:len(senti)]
    ytd_str = df_com['YTD'].values
    ytd = []
    for i, s in enumerate(ytd_str):
        if s[0] == '-':
            neg = 1
        else:
            neg = 0
        s = s.strip('%').strip('+').strip('-')
        s = float(s)
        if neg == 1:
            s *= -1
        s *= 0.01
        ytd.append(s)
    ytd = np.array(ytd)
    ytd = ytd[:len(senti)]

    # plot
    if 1:
        idx = senti_valid # & np.array(sector=='Materials')
        senti1 = senti_all[idx]
        ytd1 = ytd[idx]
        for i in range(len(feature_names)):
            plt.figure()
            plt.plot(senti1[:,i], ytd1, 'b*')
            plt.xlabel('feature: ' + feature_names[i], fontsize=15)
            plt.ylabel('YTD', fontsize=15)
            rho = np.corrcoef(senti1[:,i], ytd1)[0, 1]
            plt.title('correlation coefficient: %.3f' % rho, fontsize=15)
            # plt.savefig('output/all_industry/'+feature_names[i]+'.png')
            plt.show()

    df_data = np.concatenate((senti_all, senti_valid.reshape(-1,1), ytd.reshape(-1,1), sector.reshape(-1,1)), axis=1)
    df = pd.DataFrame(df_data, columns=feature_names+['row_valid_index', 'ytd', 'sector'])
    df.to_csv('processed_data.csv')

if __name__ == '__main__':
    main()
