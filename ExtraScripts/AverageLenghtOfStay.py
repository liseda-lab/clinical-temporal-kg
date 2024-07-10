import DataSetConstruction.TemporalFacts.AnnotationFunctions as AF
import matplotlib.pyplot as plt

stays = AF.IdGeneratorTimes("DataSetConstruction/MimicFiles/")
lengths = []
for k,v in stays.items():
    lengths.append(AF.calculateLenghtofStay(v[0], v[1])/1440)

def dispersionGraph(totalTerms):
    #get the data on the files
    data = totalTerms

    fig, ax = plt.subplots(figsize=(15, 7))
    bp = ax.boxplot(data, patch_artist=True, notch='True', vert=0)

    colors = ['#2471A3', '#F39C12', '#2ECC71', '#E74C3C']
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)


    title = f'Lenght of stay'
    plt.title(title)
 
    # Removing top axes and right axes
    # ticks
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
    
    file_name = f'LenghtOfStay!.png'  # The name of the file to save
    fig.savefig(file_name, dpi=300, bbox_inches='tight')

dispersionGraph(lengths)

plt.bar(lengths, lengths)
plt.show()