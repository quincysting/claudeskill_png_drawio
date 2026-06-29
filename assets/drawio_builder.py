"""DrawioBuilder — write a layout once with simple helpers, get an editable .drawio.

    from drawio_builder import DrawioBuilder
    d = DrawioBuilder(w=1672, h=945, bg_png="orig.png", shadow_ids={"g_a"})
    d.grp("g_a","Stage A",10,40,200,200, "#2563EB")
    d.aws("s1","S3",20,60,"s3",40)
    d.box("b1","Note",20,120,180,30, fill="#FFFFFF", stroke="#2563EB")
    d.edge("g_a","g_b","flow")
    d.save("out.drawio")

Borders are auto-softened and labels auto-escaped. Pass bg_png to embed the
original image as a locked, faded reference layer (hidden by default; toggle in
the Layers panel to diff). Identical method names to PptxBuilder, so one
layout(d) function renders to either backend.
"""
import html, base64, os, sys
from xml.dom import minidom
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from aws_icons import AWS4, CAT, soft


class DrawioBuilder:
    def __init__(self, w=1672, h=945, bg_png=None, bg_opacity=30, shadow_ids=()):
        self.W, self.H = w, h
        self.bg_png, self.bg_opacity = bg_png, bg_opacity
        self.shadow = set(shadow_ids)
        self.cells = []
        self.GEO = {}
        self._n = 0

    def _e(self, s): return html.escape(str(s), quote=True)
    def _add(self, s): self.cells.append(s)
    def _uid(self): self._n += 1; return f"_a{self._n}"

    def box(self, id, label, x, y, w, h, fill="#FFFFFF", stroke="#2D3748", font=8,
            fc="#1A202C", bold=0, align="center", valign="middle"):
        self._add(f'<mxCell id="{id or self._uid()}" value="{self._e(label)}" '
                  f'style="rounded=1;whiteSpace=wrap;html=1;fillColor={fill};strokeColor={soft(stroke,0.45)};'
                  f'strokeWidth=0.5;fontSize={font};fontColor={fc};fontStyle={bold};align={align};'
                  f'verticalAlign={valign};arcSize=8;" vertex="1" parent="rec">'
                  f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')
        if id: self.GEO[id] = (x, y, w, h)

    def grp(self, id, label, x, y, w, h, stroke, fill="none", font=9):
        sh = "shadow=1;" if id in self.shadow else ""
        self._add(f'<mxCell id="{id}" value="{self._e(label)}" '
                  f'style="rounded=1;whiteSpace=wrap;html=1;fillColor={fill};strokeColor={soft(stroke,0.3)};'
                  f'strokeWidth=0.7;{sh}fontSize={font};fontColor={stroke};fontStyle=1;verticalAlign=top;'
                  f'align=center;spacingTop=3;arcSize=5;" vertex="1" parent="rec">'
                  f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')
        self.GEO[id] = (x, y, w, h)

    def band(self, id, label, x, y, w, h, c, font=10, fc="#FFFFFF"):
        self._add(f'<mxCell id="{id or self._uid()}" value="{self._e(label)}" '
                  f'style="rounded=2;whiteSpace=wrap;html=1;fillColor={c};strokeColor={c};fontSize={font};'
                  f'fontColor={fc};fontStyle=1;align=center;verticalAlign=middle;arcSize=16;" vertex="1" parent="rec">'
                  f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')
        if id: self.GEO[id] = (x, y, w, h)

    def txt(self, id, label, x, y, w, h=16, font=10, bold=1, align="left", fc="#1A202C"):
        self._add(f'<mxCell id="{id or self._uid()}" value="{self._e(label)}" '
                  f'style="text;html=1;fontSize={font};fontStyle={bold};fontColor={fc};align={align};'
                  f'verticalAlign=middle;" vertex="1" parent="rec">'
                  f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')
        if id: self.GEO[id] = (x, y, w, h)

    def aws(self, id, label, x, y, svc, sz=32, catov=None):
        if svc not in AWS4:
            return self.box(id, label, x, y, sz, sz, "#FFFFFF", "#FF9900", 7)
        res, cat = AWS4[svc]; cat = catov or cat; fill, grad = CAT[cat]
        self._add(f'<mxCell id="{id or self._uid()}" value="{self._e(label)}" '
                  f'style="sketch=0;outlineConnect=0;fontColor=#232F3E;gradientColor={grad};gradientDirection=north;'
                  f'fillColor={fill};strokeColor=#ffffff;verticalLabelPosition=bottom;verticalAlign=top;align=center;'
                  f'html=1;fontSize=6;aspect=fixed;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.{res};" '
                  f'vertex="1" parent="rec"><mxGeometry x="{x}" y="{y}" width="{sz}" height="{sz}" as="geometry"/></mxCell>')
        if id: self.GEO[id] = (x, y, sz, sz)

    def emoji(self, glyph, cx, cw, y, sz):
        self._add(f'<mxCell id="{self._uid()}" value="{self._e(glyph)}" '
                  f'style="text;html=1;fontSize={sz-8};align=center;verticalAlign=middle;" vertex="1" parent="rec">'
                  f'<mxGeometry x="{round(cx+cw/2-sz/2)}" y="{y}" width="{sz}" height="{sz}" as="geometry"/></mxCell>')

    def ic_tb(self, idp, svc, lab, cx, cw, y, sz=32, catov=None):
        """Icon (AWS alias) or emoji centred, with a label below."""
        if svc in AWS4:
            self.aws(idp, "", round(cx + cw / 2 - sz / 2), y, svc, sz, catov)
        else:
            self.emoji(svc, cx, cw, y, sz)
        self.box(idp + "t", lab, round(cx), y + sz + 1, round(cw), 22, "none", "none", 6, align="center", valign="top")

    def ellipse(self, id, glyph, x, y, w, h, stroke, fc="#111111", font=14):
        self._add(f'<mxCell id="{id or self._uid()}" value="{self._e(glyph)}" '
                  f'style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor={stroke};strokeWidth=2;'
                  f'fontSize={font};fontColor={fc};" vertex="1" parent="rec">'
                  f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')

    def pcard(self, idp, emo, title, desc, x, y, w, h, c):
        """Persona card: round emoji badge left + bold title + description right."""
        self.box(idp, "", x, y, w, h, "#FFFFFF", c, 7)
        self.ellipse(idp + "b", emo, x + 8, round(y + h / 2 - 15), 30, 30, c)
        self.box(idp + "tt", title, x + 46, y + 6, w - 50, 16, "none", "none", 8, fc="#1A202C", bold=1, align="left", valign="middle")
        self.box(idp + "td", desc, x + 46, y + 22, w - 50, h - 26, "none", "none", 7, fc="#5B6B7B", align="left", valign="top")

    def bv(self, idp, glyph, lab, cx, cw, y, color):
        """Circular value badge (emoji) + label below."""
        self.ellipse(idp, glyph, round(cx + cw / 2 - 15), y, 30, 30, color, fc=color)
        self.box(idp + "t", lab, round(cx), y + 32, round(cw), 24, "none", "none", 6, align="center", valign="top", fc="#1A202C")

    def edge(self, s, d, label="", dashed=False):
        if s not in self.GEO or d not in self.GEO:
            return
        st = "dashed=1;" if dashed else ""
        self._add(f'<mxCell id="e_{s}_{d}" value="{self._e(label)}" '
                  f'style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;strokeColor=#6B7B8C;strokeWidth=1.4;'
                  f'endArrow=block;fontSize=7;fontColor=#37474F;labelBackgroundColor=#FFFFFF;fontStyle=1;{st}" '
                  f'edge="1" parent="rec" source="{s}" target="{d}"><mxGeometry relative="1" as="geometry"/></mxCell>')

    def save(self, path):
        body = "\n".join(self.cells)
        bg = ""
        if self.bg_png and os.path.exists(self.bg_png):
            b64 = base64.b64encode(open(self.bg_png, "rb").read()).decode()
            bg = (f'<mxCell id="bglayer" value="Original (reference)" style="locked=1;" visible="0" parent="0"/>'
                  f'<mxCell id="bgimg" value="" style="shape=image;verticalLabelPosition=bottom;verticalAlign=top;'
                  f'imageAspect=0;aspect=fixed;image=data:image/png,{b64};opacity={self.bg_opacity};" vertex="1" '
                  f'parent="bglayer"><mxGeometry x="0" y="0" width="{self.W}" height="{self.H}" as="geometry"/></mxCell>')
        doc = (f'<mxfile host="app.diagrams.net" version="24.0.0"><diagram name="Diagram" id="d1">'
               f'<mxGraphModel dx="1400" dy="900" grid="0" gridSize="10" guides="1" tooltips="1" connect="1" '
               f'arrows="1" fold="1" page="1" pageScale="1" pageWidth="{self.W}" pageHeight="{self.H}" math="0" shadow="0">'
               f'<root><mxCell id="0"/>{bg}<mxCell id="rec" value="Recreation" parent="0"/>\n{body}\n'
               f'</root></mxGraphModel></diagram></mxfile>')
        # Well-formedness check on our OWN generated string (no DOCTYPE/entities) —
        # catches unescaped & < > in labels before draw.io silently truncates.
        minidom.parseString(doc)
        open(path, "w").write(doc)
        return path
