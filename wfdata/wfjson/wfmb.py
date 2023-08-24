def mat_id_to_str(mat):
    if mat == "9":
        return "Spark Element"
    elif mat == "10":
        return "Zap Element"
    elif mat == "11":
        return "Thunderbolt Element"
    elif mat == "99":
        return "Dreamer's Crest"


class WfMbNodeJson:
    def __init__(self, data):
        self.id = data[0]
        # TODO: I don't know what the 2nd element of the node data is.
        self.mats = data[2].split(",")
        self.mat_amounts = list(map(int, data[3].split(",")))
        self.mana_cost = int(data[4])
        # TODO: I don't know what the 5th element of the node data is.
        # 6th element of node data refers to the level requirement for the node that
        # can be found in "level_required_mana_node.json".


class WfMbJson:
    def __init__(self, data):
        self.mb1_nodes = []
        self.mb2_nodes = []
        mb1 = data["1"]
        for node_key in mb1:
            node = mb1[node_key][0]
            self.mb1_nodes.append(WfMbNodeJson(node))
        if "2" in data:
            mb2 = data["2"]
            for node_key in mb2:
                node = mb2[node_key][0]
                self.mb2_nodes.append(WfMbNodeJson(node))