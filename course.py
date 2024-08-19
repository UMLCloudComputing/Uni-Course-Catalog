import requests
import concurrent.futures
import src.app.db as db
import argparse

prefixes = [
    "ACCT",
    "AERO",
    "AEST",
    "AMHE",
    "AMST",
    "ARCH",
    "ARHI",
    "ARTS",
    "ASAM",
    "ATMO",
    "BIOL",
    "BMBT",
    "BMEN",
    "BMSC",
    "BOST",
    "BUSI",
    "CHEM",
    "CHEN",
    "CIVE",
    "COMP",
    "CONT",
    "CORE",
    "CRIM",
    "DART",
    "DGMD",
    "DPTH",
    "ECON",
    "EDUC",
    "EECE",
    "ENGL",
    "ENGN",
    "ENGY",
    "ENTR",
    "ENVE",
    "ENVI",
    "ENVS",
    "ETEC",
    "EXER",
    "FAHS",
    "FINA",
    "GEOL",
    "GLST",
    "GNDR",
    "GRFX",
    "HIST",
    "HONR",
    "HSCI",
    "IENG",
    "IM",
    "INFO",
    "LABR",
    "LGST",
    "LIFE",
    "LMUCM",
    "MARI",
    "MATH",
    "MECH",
    "MGMT",
    "MIST",
    "MKTG",
    "MLSC",
    "MPAD",
    "MSIT",
    "MTEC",
    "MUAP",
    "MUBU",
    "MUCM",
    "MUED",
    "MUEN",
    "MUHI",
    "MUPF",
    "MUSR",
    "MUTH",
    "NONC",
    "NURS",
    "NUTR",
    "PCST",
    "PHIL",
    "PHRM",
    "PHYS",
    "PLAS",
    "POLI",
    "POLY",
    "POMS",
    "PSMA",
    "PSYC",
    "PTEC",
    "PUBH",
    "RADI",
    "ROTC",
    "SCIE",
    "SOCI",
    "THEA",
    "UGTC",
    "UMLO",
    "UNCR",
    "UTCH",
    "WLAN",
    "WLAR",
    "WLCH",
    "WLFR",
    "WLGE",
    "WLIT",
    "WLKH",
    "WLLA",
    "WLPO",
    "WLSP",
    "WORC",
]

def get_json(prefix, prefix_dict):
    result = requests.get(f"https://www.uml.edu/api/registrar/course_catalog/v1.0/courses?field=subject&query={prefix}")
    prefix_dict[prefix] = result.json()

def create_dict():
    prefix_dict = {}
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for prefix in prefixes:
            executor.submit(get_json, prefix, prefix_dict)
    
    return prefix_dict

# print(create_dict()["COMP"])

def insert_department(prefix):
    course_dict = create_dict()
    print(course_dict[prefix])
    with concurrent.futures.ThreadPoolExecutor() as executor:    
        for course in course_dict[prefix]:
            executor.submit(db.insert_course, course)

def insert_all():
    course_dict = create_dict()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for prefix in prefixes:
            for course in course_dict[prefix]:
                executor.submit(db.insert_course, course)
def main():
    parser = argparse.ArgumentParser(description="Insert courses into the database")
    parser.add_argument("--prefix", type=str, help="The prefix of the department")
    args = parser.parse_args()

    if args.prefix:
        insert_department(args.prefix)
    else:
        insert_all()

if __name__ == "__main__":
    main()