# Modify Below

SourceObjectID = "179"
SourceID = "15"
ConfigurationID = "15"
LineOfBusiness = "sobeys/merchandising"
SourceObjectName = "item_listings"

delimiter = ","
encoding = "UTF-8"
fileFormat = "csv"
compressionMode = ""
skiphead = "1"
truncate = ""
key = "Assortment, ItemSku, ValidFrom"
quoteChar = "\\\""
isencrypted = ""
tableType = "dimension"

Frequency = "1"
FrequencyDurationUnit = "DAY"
CreatedBy = "adminsql"
CreatedOn = "getdate()"
ModifiedBy = "adminsql"
ModifiedOn = "getdate()"

IsActive = "1"
SinkObjectName = "ItemListings"
LandingToRawFlag = "0"
CopyFromRawFlag = "0"

# Don't modify anything below

def create_raw_mapping(column):
  with open(f'GenerateSourceObjectDetails\{column}.txt') as f:

    lines = f.readlines()
    list_output = []

    for i in lines:
        list_output.append(i.replace("\n", ""))

  final_list = list(filter(None, list_output))

  return final_list

name = create_raw_mapping('name_list')
type = create_raw_mapping('type_list')

merge_type_name = list(map(list, zip(name, type)))

if len(type) == len(name):
  with open('ObjectProperties.txt', 'w') as f:

    f.write("INSERT into Metadata.SourceObjectdetail\n(SourceObjectID,SourceID, ConfigurationID, LineOfBusiness, SourceObjectName, ObjectProperties, Frequency, FrequencyDurationUnit, CreatedBy,CreatedOn,ModifiedBy, ModifiedOn, RawMapping, IsActive, SinkObjectName, LandingToRawFlag, CopyFromRawFlag)\nVALUES(\n")

    f.write(f"{SourceObjectID},\n")
    f.write(f"{SourceID},\n")
    f.write(f"{ConfigurationID},\n")

    f.write(f"\'{LineOfBusiness}\',\n")
    f.write(f"\'{SourceObjectName}\',\n")

    f.write("\'{\n	\"initial\": {\n		\"delimiter\": \"%s\",\n		\"encoding\": \"%s\",\n		\"fileFormat\": \"%s\",\n		\"compressionMode\": \"%s\",\n		\"skiphead\": \"%s\",\n		\"truncate\": \"%s\",\n		\"key\": \"%s\",\n		\"quoteChar\": \"%s\",\n		\"isencrypted\": \"%s\"\n	},\n	\"tableType\": \"%s\"\n}',\n" % (delimiter, encoding, fileFormat, compressionMode, skiphead, truncate, key, quoteChar, isencrypted, tableType))

    f.write(f"{Frequency},\n")
    f.write(f"\'{FrequencyDurationUnit}\',\n")
    f.write(f"\'{CreatedBy}\',\n")
    f.write(f"{CreatedOn},\n")
    f.write(f"\'{ModifiedBy}\',\n")
    f.write(f"{ModifiedOn},\n")


    f.write("\'{\n   \"type\": \"TabularTranslator\",\n   \"mappings\":[")

    # Raw Mapping Generator
    for i in range(len(merge_type_name)):
      if i < len(merge_type_name) - 1:
        f.write("\n {\n   \"source\": {\n      \"type\": \"%s\",\n      \"ordinal\": %d\n   },\n   \"sink\": {\n      \"name\": \"%s\"\n   }\n}," % (merge_type_name[i][1], i + 1, merge_type_name[i][0]) )
      else:
        f.write("\n {\n   \"source\": {\n      \"type\": \"%s\",\n      \"ordinal\": %d\n   },\n   \"sink\": {\n      \"name\": \"%s\"\n   }\n}" % (merge_type_name[i][1], i + 1, merge_type_name[i][0]) )

    f.write("\n]\n}',\n")

    f.write(f"{IsActive},\n")
    f.write(f"\'{SinkObjectName}\',\n")
    f.write(f"{LandingToRawFlag},\n")
    f.write(f"{CopyFromRawFlag}\n")

    f.write(")\nGO")

  f.close()
else:
  print("List is not the same length")
