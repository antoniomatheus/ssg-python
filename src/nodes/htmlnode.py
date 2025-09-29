class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if not self.props:
            return ""
        
        attributes = ""
        for key, value in self.props.items():
            attributes += f" {key}=\"{value}\""
        return attributes
    
    def __repr__(self):
        return f"""HTMLNode(
            {self.tag},
            {self.value}
            {self.children}
            {self.props}
        )"""