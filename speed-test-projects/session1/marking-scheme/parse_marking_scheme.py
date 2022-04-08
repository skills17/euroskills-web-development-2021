#!/usr/bin/env python
# coding: utf-8

# This python script read the MARKING.md and convert the custom format into marking scheme excel.
#
# Format:
#
# ```
#
# Format:
#
# ## {Subcriterion ID} {Subcriterion description}
# day:: 1
#
# ### {Aspect type} {Aspect description}
# mark:: 1
# wsss:: 3
#
# extra description. in multiple lines
#
# ### J {Aspect description}
# mark:: 1
# wsss:: 1
#
# 0. Judgement description
# 1. Judgement description
# 2. Judgement description
# 3. Judgement description
#
# ## {Subcriterion ID} {Subcriterion description}
# day:: 1
#
# ### M another aspect
# mark:: 1
# wsss:: 1
#
# Continue with other `##` subcriterion and `###` marking aspect.
# ```

# In[134]:


#!pip install markdown


# In[108]:


from collections import namedtuple

SubCriterion = namedtuple("SubCriterion", ["id", "description", "day_of_marking", "aspects"])

MarkingAspect = namedtuple("MarkingAspect", ["type", "description", "extra_description", "requirement", "wsos", "max_mark", "judgement_descriptions"])


# In[109]:


def is_sub_criterion(text):
    return text[:3] == "## "
def is_aspect(text):
    return text[:4] == "### "


# In[110]:


import markdown
from bs4 import BeautifulSoup

file = "MARKING.md"

with open(file, encoding="utf-8") as f:
    raw_text = f.read().split("----")[0].strip()

raw_text = raw_text.replace("\n\n\n\n","\n\n").replace("\n\n\n", "\n\n")

#print(raw_text)



# In[ ]:





# In[111]:


marking_groups = []

groups = raw_text.split("\n\n")

current_sub_criterion = []
current_aspect = []

for g in groups:
    if is_sub_criterion(g):
        marking_groups.append([g])
        #if len(current_sub_criterion) > 0:
        #    current_sub_criterion.append(current_aspect)
        #    marking_groups.append(current_sub_criterion)
        #    current_sub_criterion = []

        #current_sub_criterion.append(g)
        #current_sub_criterion.append(current_aspect)
    elif is_aspect(g):
        marking_groups[-1].append([g])
        #if len(current_aspect) > 0:
        #    current_sub_criterion.append(current_aspect)
        #    current_aspect = []
        #current_aspect.append(g)
    else:
        marking_groups[-1][-1].append(g)
        #current_aspect.append(g)

# the last one
#current_sub_criterion.append(current_aspect)
#marking_groups.append(current_sub_criterion)


# In[115]:


# Transform to namedtuple

marking_scheme = []

for group in marking_groups:
    line1 = group[0].split("\n")[0]
    line1 = line1.replace("## ","")
    cid = line1.split(" ")[0]
    name = " ".join(line1.split(" ")[1:])
    day = group[0].split("\n")[-1].split(":: ")[-1]
    aspects = []

    for items in group[1:]:
        heading = items[0].replace("### ","")
        line1 = heading.split("\n")[0]
        marking_type = line1[0]
        description = line1[2:]
        mark = heading.split("\n")[1].split(":: ")[-1]
        wsss = heading.split("\n")[2].split(":: ")[-1]

        if marking_type == "J":
            extra = "\n".join(items[1:-1])
            judgement_descriptions = items[-1].split("\n")
        else:
            extra = "\n".join(items[1:])
            judgement_descriptions = []

        aspects.append(MarkingAspect(
            type = marking_type,
            description = description,
            extra_description = extra,
            requirement = "",
            wsos = wsss,
            max_mark = float(mark),
            judgement_descriptions = judgement_descriptions
        ))


    marking_scheme.append(SubCriterion(cid, name, day, aspects))

    #print("----")


# In[116]:



#for ms in marking_scheme:
#    print(ms.id, ms.description)
#    print("Day", ms.day_of_marking)
#    print()
#    for aspect in ms.aspects:
#        print(aspect.type)
#        print(aspect.max_mark)
#        print(aspect.description)
#        print(aspect.extra_description)
#        print(aspect.judgement_descriptions)
#        print()


# Next, save export to Excel

# In[133]:


import openpyxl

wb = openpyxl.load_workbook("marking_scheme_template.xlsx")

# grab the active worksheet
ws = wb.active

#ws.append([
#    "Sub Criterion ID",
#    "Sub Criterion Name or Description",
#    "Day of Marking",
#    "Aspect Type\nM\nJ",
#    "Aspect - Description",
#    "Judge Score",
#    "Extra Aspect Description (Meas or Judg) OR Judgement Score Description (Judg only)",
#    "Requirement (Measurement Only)",
#    "WSSS Section",
#    "Calculation Row (Export only)",
#    "Max Mark"
#])



for ms in marking_scheme:
    ws.append([ms.id, ms.description, ms.day_of_marking])

    for aspect in ms.aspects:
        if aspect.type == "J":
            ws.append([""])

        ws.append(["","","",
                       aspect.type,
                       aspect.description,
                       "",
                       aspect.extra_description,
                       "",
                       aspect.wsos,
                       "",
                       aspect.max_mark
                  ])
        if aspect.type == "J":
            judgement_descriptions = aspect.judgement_descriptions
            judgement_descriptions = [(x[0], x[2:]) for x in judgement_descriptions]

            for i in range(4):
                ws.append(["","","","","",
                           judgement_descriptions[i][0],
                           judgement_descriptions[i][1]
                          ])
            ws.append([""])

wb.save("marking.xlsx")
print("Saved to marking.xlsx.")


# In[ ]:





# In[ ]:





# --------

# import markdown
# from bs4 import BeautifulSoup
#
# file = "MARKING.md"
#
# with open(file, encoding="utf-8") as f:
#     raw_text = f.read().split("----")[0]
#
#
# text = markdown.markdown(raw_text)
# soup = BeautifulSoup(text, "lxml")
#
# marking_groups = []
#
#
# for element in soup.select_one("body").children:
#     if element.name == None:
#         continue
#     #print(element.name)
#     if element.name == "h2":
#         if len(current_criterion.aspects) > 0:
#             marking_groups.append(current_criterion)
#         id = element.text.split(" ")[0]
#         name = " ".join(element.text.split(" ")[1:])
#         current_criterion = SubCriterion(id, name, 0, [])
#         print(current_criterion)
#     elif element.name == "h3":
#         if len(new_aspect) > 0:
#             new_group.append(new_aspect)
#         current_aspect =
#     else:
#         new_aspect.append(element)
#
#
# for group in marking_groups:
#     for aspect in group:
#
#         print(aspect)