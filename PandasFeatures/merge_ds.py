# -*- coding: utf-8 -*-
"""
Merging of dataframes in Python
"""

# import libraries
import os
import pandas as pd

pd.set_option('display.max_columns' ,100)

usage_path = os.path.abspath("Data/MergeDS/user_usage.csv")
device_path = os.path.abspath("Data/MergeDS/user_device.csv")
android_path = os.path.abspath("Data/MergeDS/android_devices.csv")

# user_usage DataSet
user_usage = pd.read_csv(usage_path)
user_usage.columns
user_usage.info()
user_usage.head()
 
# user_device Dataset
user_device = pd.read_csv(device_path)
user_device.columns
user_device.info()
user_device.head()

#android_device Dataset
devices = pd.read_csv(android_path)
devices.columns
devices.info()
devices.head()

#---------------------------------------------------
"""
MERGE --INNER DEFAULT -- We're trying to get the average usage figures for different types of 
devices. So we need to get the user's device code from user_usage as a column 
on user_usage, and then get the device's manufacturer from devices as a column 
on the result.
First, we merge user_usage with user_device with "use_id" as our common column
"""
result = pd.merge(user_usage, user_device[['use_id','platform','device']], 
                  on='use_id')

result.head()

print("user_usage dimensions: {}".format(user_usage.shape))
print("user_device dimensions: {}".format(
        user_device[['use_id','platform','device']].shape))

print("result dimesion : {}".format(result.shape))
#---------------------------------------------------
"""
LEFT MERGE - between two dataframes keeps all of the rows and values from the 
left dataframe, in this case "user_usage". Rows from the right dataframe will 
be kept in the result only where there is a match in the merge variable in the
right dataframe, and NaN values will be in the result where not.
"""
result = pd.merge(user_usage,user_device[['use_id','platform','device']],
                  on='use_id', how='left')

print("user_usage dimensions: {}".format(user_usage.shape))
print("user_device dimensions: {}".format(
        user_device[['use_id','platform','device']].shape))
print("result dimesion : {}".format(result.shape))
print("There are {} missing values in the result".format(result['device'].
      isnull().sum()))

result.head()
#---------------------------------------------------
"""
RIGHT MERGE, or right join, between two dataframes keeps all of the rows and
values from the right dataframe, in this case "user_device". 
Rows from the left dataframe will be kept where there is a match in the merge 
variable, and NaN values will be in the result where not.
"""
result = pd.merge(user_usage,user_device[['use_id','platform','device']],
                  on='use_id', how='right')
print("user_usage dimensions: {}".format(user_device.shape))
print("result dimesion : {}".format(result.shape))
print("There are {} missing values in the 'monthly_mb' result".
      format(result['monthly_mb'].isnull().sum()))
print("There are {} missing values in the 'platform' result".
      format(result['platform'].isnull().sum()))

#---------------------------------------------------
"""
OUTER MERGE
A full outer join keeps all rows from the left and right dataframe in the result.
Rows will be aligned where there is shared join values
between the left and right, and rows with NaN values, in either the 
left-originating or right-originating columns will be, will be left in the 
result where there is no shared join value.

In the final result, a subset of rows should have no missing values. 
These rows are the rows where there was a match between the merge column in 
the left and right dataframes. These rows are the same values as found by our 
inner merge result before.
"""
print("There are {} unique values of use_id in our dataframes.".format(
        pd.concat([user_usage['use_id'], user_device['use_id']]).unique().shape[0]))
result = pd.merge(user_usage,
                 user_device[['use_id', 'platform', 'device']],
                 on='use_id', how='outer', indicator=True)

print("Outer merge result has {} rows.".format(result.shape))

print("There are {} rows with no missing values.".format(
    (result.apply(lambda x: x.isnull().sum(), axis=1) == 0).sum()))

result.iloc[[0,1,200,201,350,351]]

#---------------------------------------------------
"""
FINAL MERGE -- Adding device manufacturer
"""

# First, add the platform and device to the user usage.
result = pd.merge(user_usage,
                 user_device[['use_id', 'platform', 'device']],
                 on='use_id',
                 how='left')

# Now, based on the "device" column in result, match the "Model" column in devices.
devices.rename(columns={"Retail Branding": "manufacturer"}, inplace=True)
result = pd.merge(result, 
                  devices[['manufacturer', 'Model']],
                  left_on='device',
                  right_on='Model',
                  how='left')

result.head()

devices[devices.Model == 'SM-G930F']

devices[devices.Device.str.startswith('GT')]
#---------------------------------------------------
# Calculating statistics on final result

result.groupby("manufacturer").agg({
        "outgoing_mins_per_month":"mean",
        "outgoing_sms_per_month": "mean",
        "monthly_mb": "mean",
        "use_id": "count"
        })












































