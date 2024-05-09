from flask import Flask, render_template
import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO, BytesIO
import base64
from flask_frozen import Freezer

app = Flask(__name__)
freezer = Freezer(app)

# CSV data
csv_data = '''prover,job_name,job_size,proof_duration_microsec,verify_duration_microsec,proof_bytes
miden,iter_blake3,1,342283,419,67000
miden,iter_blake3,10,884350,423,83391
miden,iter_blake3,100,3568577,444,101331
miden,iter_sha2,1,389440,457,72941
miden,iter_sha2,10,1381348,414,89572
miden,iter_sha2,100,5684549,448,107565
miden,iter_rescue_prime,1,137763,2780,53203
miden,iter_rescue_prime,10,126569,2286,53284
miden,iter_rescue_prime,100,217742,2312,57529
miden,iter_rescue_prime,1000,565164,2657,72742
risczero,big_sha2,4096,1889546,2413,217448
risczero,big_sha2,8192,3814567,2619,229160
risczero,big_sha2,16384,7611628,2598,241384
risczero,big_sha2,32768,15161667,2732,254632
risczero,iter_sha2,1,209847,2134,172136
risczero,iter_sha2,10,450156,2173,182760
risczero,iter_sha2,100,3635788,2508,229160'''

@app.route('/')
def index():
    # Convert the CSV data into a pandas DataFrame
    df = pd.read_csv(StringIO(csv_data))

    # Group by 'prover' and 'job_size' and calculate the average verify duration
    verify_grouped = df.groupby(['prover', 'job_size'])['verify_duration_microsec'].mean().reset_index()

    # Pivot the DataFrame for plotting
    verify_pivot_df = verify_grouped.pivot(index='job_size', columns='prover', values='verify_duration_microsec')

    # Plot the verify data with specified colors
    ax1 = verify_pivot_df.plot(kind='bar', figsize=(10, 6), color=['#006C84', '#EDE574'])
    plt.title('Average Verify Duration by Job Size and Prover')
    plt.xlabel('Job Size')
    plt.ylabel('Average Verify Duration (microseconds)')
    plt.xticks(rotation=0)
    plt.legend(title='Prover')

    # Save verify plot to a BytesIO object
    verify_img = BytesIO()
    plt.savefig(verify_img, format='png')
    verify_img.seek(0)
    
    # Embed verify plot into HTML
    verify_plot_url = base64.b64encode(verify_img.getvalue()).decode()

    # Group by 'prover' and 'job_size' and calculate the average proof duration
    proof_grouped = df.groupby(['prover', 'job_size'])['proof_duration_microsec'].mean().reset_index()

    # Pivot the DataFrame for plotting
    proof_pivot_df = proof_grouped.pivot(index='job_size', columns='prover', values='proof_duration_microsec')

    # Plot the proof data
    ax2 = proof_pivot_df.plot(kind='bar', figsize=(10, 6), color=['#006C84', '#EDE574'])
    plt.title('Average Proof Duration by Job Size and Prover')
    plt.xlabel('Job Size')
    plt.ylabel('Average Proof Duration (microseconds)')
    plt.xticks(rotation=0)
    plt.legend(title='Prover')

    # Save proof plot to a BytesIO object
    proof_img = BytesIO()
    plt.savefig(proof_img, format='png')
    proof_img.seek(0)
    
    # Embed proof plot into HTML
    proof_plot_url = base64.b64encode(proof_img.getvalue()).decode()

    return render_template('index.html', verify_plot_url=verify_plot_url, proof_plot_url=proof_plot_url)

if __name__ == '__main__':
    freezer.freeze()
