

# def processOutputItem(originalData, inputData, outputItemCheck, keyCheck, valueCheck):
#     # if outputItemCheck == "" or keyCheck == "" or valueCheck == "":
#     #     return []
#
#     outputLines = []
#
#     try:
#         for outputItem in list(inputData.index):
#             if outputItem == outputItemCheck:
#                 for key in originalData.keys():
#                     if keyCheck in key:
#                         if type(originalData[key]) == dict:
#                             value = originalData[key][valueCheck]
#                         else:
#                             # print((originalData[key]))
#                             value = originalData[key]
#                         outputLines.append(f"{outputItem};{key};{str(value)}")
#
#         return outputLines
#     except Exception as e:
#         print(e)
#         return [traceback.format_exc()]
#