
class baseModel:
    def __init__(self, node_num, node_offset, local_node_offset):
        ### TODO
        self.node_num           = node_num
        self.node_offset        = node_offset
        self.local_node_offset  = local_node_offset
        self.local_node_list    = None
        self.route_table        = None
        self.link_util          = None
        
    def makeTopology(self):
        pass
    
    def makeRouteTable(self):
        pass
    
    def makeInterconnection(self):
        pass
    
    def printDebug(self):
        pass
        
class Mesh2DModel(baseModel):
    def __init__(self, node_x, node_y, link_BW, node_BW, link_e, node_link_e node_offset, local_node_offset):
        super().__init__(node_x * node_y, node_offset, local_node_offset)
        self.x_dim       = node_x
        self.y_dim       = node_y
        self.link_BW     = link_BW
        self.node_BW     = node_BW
        self.link_e      = link_e
        self.node_link_e =node_link_e
    
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
                    self.link_util[(node_id, node_up)] = [0, self.link_BW, self.link_e]
                    self.link_util[(node_up, node_id)] = [0, self.link_BW, self.link_e]
                # -- right node
                if x < self.x_dim - 1:
                    node_right =  self.getNodeId(x+1, y)
                    self.link_util[(node_id, node_right)] = [0, self.link_BW, self.link_e]
                    self.link_util[(node_right, node_id)] = [0, self.link_BW, self.link_e]
                # -- local node
                node_local = self.getNodeId(x, y, local=1)
                self.link_util[(node_id, node_local)] = [0, self.node_BW, self.node_link_e]
                self.link_util[(node_local, node_id)] = [0, self.node_BW, self.node_link_e]
                
                self.local_node_list.append(node_local)
    
    def XYRoute(self, src, dst):
        route = []
        src_node = src - self.local_node_offset
        dst_node = dst - self.local_node_offset
        
        # 1. go to the interconnection network node
        route.append((src, src_node))
        
        # 2. go through the interconnection network
        src_x , src_y = self.getXYIdx(src)
        dst_x , dst_y = self.getXYIdx(dst)
        # --- 2.1 X Direction
        if src_x > dst_x:    # 1 : dst_x > src_x, -1 : dst_x < src_x
            tag = -1
        else:
            tag = 1
        cur_src_node = src_node
        cur_dst_node = src_node
        for x in range(src_x, dst_x, tag):
            cur_src_node = self.getNodeId(x, src_y)
            assert(cur_src_node == cur_dst_node)
            cur_dst_node = self.getNodeId(x+tag, src_y)
            route.append((cur_src_node, cur_dst_node))
        
        # --- 2.2 Y Direction
        if src_y > dst_y:    # 1 : dst_y > src_y, -1 : dst_y < src_y
            tag = -1
        else:
            tag = 1
        for y in range(src_y, dst_y, tag):
            cur_src_node = self.getNodeId(dst_x, y)
            assert cur_src_node == cur_dst_node , "cur_src_node:{}, cur_dst_node:{}, src({},{}), dst({},{})".format(cur_src_node, cur_dst_node, src_x, src_y, dst_x, dst_y)
            cur_dst_node = self.getNodeId(dst_x, y+tag)
            route.append((cur_src_node, cur_dst_node))
                   
        # 3. go to the dst node     
        route.append((dst_node, dst))
        return route
    
    def makeRouteTable(self):
        # make route table, considering XY-routing
        self.route_table = {}
        
        for src in self.local_node_list:
            for dst in self.local_node_list:
                if src == dst:
                    continue
                route = self.XYRoute(src, dst)
                self.route_table[(src, dst)] = route
    
    def makeInterconnection(self):
        self.makeTopology()
        self.makeRouteTable()

    def printDebug(self):
        print("{:-^50s}".format(" local_node_list "))
        node_list = ""
        for y in range(self.y_dim):
            for x in range(self.x_dim):
                id = x + y * self.x_dim
                node_id = self.local_node_list[id]
                node_list += str(node_id) + '\t'
            node_list += '\n'
        print(node_list)
        
        print("{:-^50s}".format(" route table "))
        for pair, route in self.route_table.items():
            print("{}: {}".format(pair, route))
        print("")
        
        print("{:-^50s}".format(" link util "))
        for pair, link in self.link_util.items():
            print("{}: {}".format(pair, link))

if __name__ == '__main__':
    node_x = 4
    node_y = 4
    link_BW = 2
    node_BW = 1
    node_offset = 0
    local_node_offset = 1000
    
    Mesh = Mesh2DModel(node_x, node_y, link_BW, node_BW, node_offset, local_node_offset)
    Mesh.makeInterconnection()
    Mesh.printDebug()
