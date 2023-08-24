from wfdata.wfjson.wfjson import WfJson

def main():
    wf_json = WfJson("wf_data_json")
    print(wf_json.characters_by_name["Beaucy"])


if __name__ == '__main__':
    main()
