
class baseModel:
    def __init__(self, node_num, node_offset, local_node_offset):
        ### TODO
        self.node_num           = node_num
        self.route_table        = None
        self.link_util          = None
        self.node_offset        = node_offset
        self.local_node_offset  = local_node_offset
        self.local_node_list    = None

class Mesh2DModel(baseModel):
    def __init__(self, node_x, node_y, link_BW, node_BW, node_offset, local_node_offset):
        self.x_dim      = node_x
        self.y_dim      = node_y
        self.node_num   = node_x * node_y
        self.link_BW    = link_BW
        self.node_BW    = node_BW
        super().__init__(node_x * node_y, node_offset, local_node_offset)
    
    def getNodeId(self, x, y, local=0):
        node_id = x + y * self.x_dim
        node_id += self.node_offset
        if local:
            node_id += self.local_node_offset
        return node_id
    
    def getXYIdx(self, node_id, local=1):
        node_id -= self.node_offset
        if local:
            node_id -= self.local_node_offset
        x_idx = node_id % self.x_dim
        y_idx = node_id // self.y_dim
        
        return x_idx, y_idx
    
    def makeTopology(self):
        # make empty link_util
        # make local_node_list
        self.link_util          = {}
        self.local_node_list    = []
        
        # - make link
        for y in range(self.y_dim):
            for x in range(self.x_dim):
                node_id = self.getNodeId(x, y)
                # -- upper node
                if y < self.y_dim - 1:
                    node_up =  self.getNodeId(x, y+1)
                    self.link_util[(node_id, node_up)] = [0, self.link_BW]
                    self.link_util[(node_up, node_id)] = [0, self.link_BW]
                # -- right node
                if x < self.x_dim - 1:
                    node_right =  self.getNodeId(x+1, y)
                    self.link_util[(node_id, node_right)] = [0, self.link_BW]
                    self.link_util[(node_right, node_id)] = [0, self.link_BW]
                # -- local node
                node_local = self.getNodeId(x, y, local=1)
                self.link_util[(node_id, node_local)] = [0, self.node_BW]
                self.link_util[(node_local, node_id)] = [0, self.node_BW]
                
                self.local_node_list.append(node_local)
    
    def makeRouteTable(self):
        # make route table
        self.route_table = {}
        
        for local_node in self.local_node_list:
            
                  
                
        