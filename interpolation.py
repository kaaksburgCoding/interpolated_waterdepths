import numpy as np
import pandas as pd

# open csv file and create iterable numpy_array out of it (10x9)
csvfile = open(r"C:\Users\Jose Matthias\Desktop\Uni\Bachelorarbeit_Inhalt\postProcessing\line5_alpha_water.csv")
numpy_array = np.loadtxt(csvfile, delimiter=";")

# get number of rows and columns of the numpy_array
n_rows = len(numpy_array)
n_columns = len(numpy_array[0])

# create empty data frame to add analysis parameters (t(s), waterdepths) later
dataframe = pd.DataFrame({'t(s)': [], 'd(m)': []})


def calculate_waterdepths(numpy_array):

   interpolated_water_depths = []

   i = 0
   j = 0

   #outer loop over 800 timesteps
   while (i < n_rows and j < n_rows):

      i=j
      print("i=", i)
      current_timestep = numpy_array[i][0]

      # empty lists to store z- and alpha-values of current timestep
      # one list for alpha-values under 0.5, one list for alpha values over 0.5
      z_alpha_smaller05 = []
      z_alpha_larger05 = []

      print("j=", j, "i=", i)
      print("soll gleich sein:", numpy_array[j][0],current_timestep )

      #inner loop over the entries of same timesteps
      while (j < n_rows and numpy_array[j][0] == current_timestep):

         # print the current entry/row
         current_row = numpy_array[j]
         print("current row", current_row)

         #declare and instanciate the 4th and 5th value of the row and z and alpha
         z = numpy_array[j][3]
         alpha = numpy_array[j][4]

         # append values to corresponding list
         if alpha < 0.5:
            z_alpha_smaller05.append([z, alpha])
            print("[z and alpha under 0.5:", z_alpha_smaller05)

         else:
            z_alpha_larger05.append([z, alpha])
            print("[z and alpha over 0.5:", z_alpha_larger05)

         # go to next row
         print ("j=",j)
         j = j+1

      print("kleines z und alpha", z_alpha_smaller05)
      print("großes z und alpha", z_alpha_larger05)

      closest_values = get_two_closest_values(z_alpha_smaller05, z_alpha_larger05)

      alpha1 = closest_values[0][1]
      alpha2 = closest_values[1][1]

      z1 = closest_values[0][0]
      z2 = closest_values[1][0]

      depth_this_timestep = interpolate(alpha1,alpha2, z1, z2)

      to_append = [current_timestep,depth_this_timestep]
      dataframe_length = len(dataframe)
      dataframe.loc[dataframe_length] = to_append

      interpolated_water_depths.append(depth_this_timestep)

      i = i+1

   return interpolated_water_depths


def get_two_closest_values(z_alpha_smaller05, z_alpha_larger05):

   closestValues = []

   value1 = max(z_alpha_smaller05, key = lambda x: x[1])
   value2 = min (z_alpha_larger05, key = lambda x: x[1])

   closestValues.append(value1)
   closestValues.append(value2)

   return closestValues

def interpolate(value1, value2, z1, z2):
   d = z1 + (0.5 - value1)*(z2-z1)/(value2-value1)
   return d

waterdepths=calculate_waterdepths(numpy_array)
print(waterdepths)
print(dataframe)

datatoexel = pd.ExcelWriter(r"C:\Users\Jose Matthias\Desktop\Uni\Bachelorarbeit_Inhalt\postProcessing\interpolated_waterdepths.xls")
dataframe.to_excel(r"C:\Users\Jose Matthias\Desktop\Uni\Bachelorarbeit_Inhalt\postProcessing\interpolated_waterdepths.xls")












