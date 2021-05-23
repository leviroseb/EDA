
class Color(object):
    def __init__(self, r=0, g=0, b=0, a=None):
        self.red = r
        self.green = g
        self.blue = b
        self.alpha = a
        
def intToBitString (integer):
        bit=""
        while(integer // 2 != 0):
            bit = str(integer % 2) + bit
            integer = integer // 2
        bit=str(integer) + bit
        bit=str("0"*(8-len(bit)))+bit
        return bit


# In[2]:


class OctreeNode(object):

    def __init__(self, level, parent):

        self.color = Color(0, 0, 0)
        self.pixel_count = 0
        self.palette_index = 0
        self.children = [None for _ in range(8)]
        if level < OctreeQuantizer.MAX_DEPTH - 1:
            parent.add_level_node(level, self)

    def is_leaf(self):
        return self.pixel_count > 0

    def getLeafs(self):
        leaf_nodes = []
        for i in range(8):
            node = self.children[i]
            if node:
                if node.is_leaf():
                    leaf_nodes.append(node)
                else:
                    leaf_nodes.extend(node.getLeafs())
        return leaf_nodes

    def getPixelCounts(self):
 
        sum_count = self.pixel_count
        for i in range(8):
            node = self.children[i]
            if node:
                sum_count += node.pixel_count
        return sum_count

    def add_color(self, color, level, parent):

        if level >= OctreeQuantizer.MAX_DEPTH:
            self.color.red += color.red
            self.color.green += color.green
            self.color.blue += color.blue
            self.pixel_count += 1
            return
        index = self.getIndex(color, level)
        if not self.children[index]:
            self.children[index] = OctreeNode(level, parent)
        self.children[index].add_color(color, level + 1, parent)

    def get_palette_index(self, color, level):
        
        if self.is_leaf():
            return self.palette_index
        index = self.getIndex(color, level)
        if self.children[index]:
            return self.children[index].get_palette_index(color, level + 1)
        else:
            for i in range(8):
                if self.children[i]:
                    return self.children[i].get_palette_index(color, level + 1)

    def remove_leaves(self):
        result = 0
        for i in range(8):
            node = self.children[i]
            if node:
                self.color.red += node.color.red
                self.color.green += node.color.green
                self.color.blue += node.color.blue
                self.pixel_count += node.pixel_count
                result += 1
        return result - 1

    def getIndex(self,color, level):
        index = 0
        r=intToBitString(color.red)
        g=intToBitString(color.green)
        b=intToBitString(color.blue)
        if r[level]=="1":
            index += 4
        if g[level]=="1":
            index += 2
        if b[level]=="1":
            index += 1
        return index

    def get_color(self):
        return Color(
            self.color.red / self.pixel_count,
            self.color.green / self.pixel_count,
            self.color.blue / self.pixel_count)


class OctreeQuantizer(object):
    MAX_DEPTH = 8

    def __init__(self):
        self.levels = {i: [] for i in range(OctreeQuantizer.MAX_DEPTH)}
        self.root = OctreeNode(0, self)

    def get_leaves(self):
        return [node for node in self.root.getLeafs()]

    def add_level_node(self, level, node):
        self.levels[level].append(node)

    def add_color(self, color):
        self.root.add_color(color, 0, self)

    def reduction(self, color_count):
        #reduccion de colores
        palette = []
        palette_index = 0
        leaf_count = len(self.get_leaves())
        for level in range(OctreeQuantizer.MAX_DEPTH -1, -1, -1):
            if self.levels[level]:
                for node in self.levels[level]:
                    leaf_count -= node.remove_leaves()
                    if leaf_count <= color_count:
                        break
                if leaf_count <= color_count:
                    break
                self.levels[level] = []
                
        # Construccion de la paleta
        for node in self.get_leaves():
            if palette_index >= color_count:
                break
            if node.is_leaf():
                palette.append(node.get_color())
            node.palette_index = palette_index
            palette_index += 1
        return palette

    def get_palette_index(self, color):
        return self.root.get_palette_index(color, 0)
    
    def fill (self,w, h,pixels):
        for j in range(h):
            for i in range(w):
                self.add_color(Color(*pixels[i, j]))

    
    def reconstruction (self,w, h,pixels,palette):
        out_image = Image.new('RGB', (w, h))
        out_pixels = out_image.load()
        index=0
        for j in range(h):
            for i in range(w):
                index = self.get_palette_index(Color(*pixels[i, j]))
                color = palette[index]
                out_pixels[i, j] = (int(color.red), int(color.green), int(color.blue))
        display(out_image)
        out_image.save('image_out.png')


# In[3]:


from PIL import Image

def main():
    image = Image.open('mirio.jpg')
    pixels = image.load()
    width, height = image.size
    
    display(image)

    octree = OctreeQuantizer()
  
    octree.fill(height, width,pixels)
    
    palette = octree.reduction(256)

    palette_image = Image.new('RGB', (16, 16))
    palette_pixels = palette_image.load()      
    for i, color in enumerate(palette):
        palette_pixels[i % 16, i / 16] = (int(color.red), int(color.green), int(color.blue))
    palette_image.save('palette.png')
    display(palette_image)

    octree.reconstruction(height,width,pixels,palette)

if __name__ == '__main__':
    main()


# In[ ]:




