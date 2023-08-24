from wfdata.wfjson.wfjson import WfJson

def main():
    wf_json = WfJson("wf_data_json")
    print(wf_json.find("Beaucy"))


if __name__ == '__main__':
    main()
