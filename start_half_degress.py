import multiprocessing
from half_degrees_multiprocessor import *
import psycopg2

'''
w = 179.5
e = 0.5
fields = []
table = "CREATE TABLE length_year_matrix_lng_half (year integer PRIMARY KEY, "

while w > 0:
  if not w.is_integer():
    toAppend = "w" + str(int(w)) + "_5 numeric"
  else :
    toAppend = "w" + str(int(w)) + " numeric"
  fields.append(toAppend)
  w -= 0.5

fields.append("xlng0 numeric")

while e < 180:
  if not e.is_integer():
    toAppend = "e" + str(int(e)) + "_5 numeric"
  else:
    toAppend = "e" + str(int(e)) + " numeric"
  fields.append(toAppend)
  e += 0.5

table += ', '.join(fields)
table += ")"



n = 89.5
s = 0.5
year = 0
table = "CREATE TABLE length_year_matrix_lat_half (year integer PRIMARY KEY, "
fields = []

while n > 0 :
  if not n.is_integer():
    toAppend = "n" + str(int(n)) + "_5 numeric"
  else :
    toAppend = "n" + str(int(n)) + " numeric"
  fields.append(toAppend)
  n -= 0.5

fields.append("xlat0 numeric")

while s < 90 :
  if not s.is_integer():
    toAppend = "s" + str(int(s)) + "_5 numeric"
  else :
    toAppend = "s" + str(int(s)) + " numeric"
  fields.append(toAppend)
  s += 0.5

table += ', '.join(fields)
table += ")"

insert = "INSERT INTO length_year_matrix_lat_half (year) VALUES "
insert_years = []
for year in xrange(0,551) :
  insert_years.append("(" + str(year) + ")")

insert += ', '.join(insert_years)

'''
if __name__ == '__main__':
  tasks = multiprocessing.JoinableQueue()
  results = multiprocessing.Queue()

  num_processors = multiprocessing.cpu_count() - 1
  processors = [Processor(tasks, results) for i in xrange(num_processors)]

  for each in processors:
    each.start()

  # Set up the tables
  connection = psycopg2.connect(dbname="alice", user="john", host="localhost", port="5432")
  cursor = connection.cursor()

  cursor.execute("""
    DROP TABLE IF EXISTS length_year_matrix_lng_half;
    CREATE TABLE length_year_matrix_lng_half (year integer PRIMARY KEY, w179_5 float8, w179 float8, w178_5 float8, w178 float8, w177_5 float8, w177 float8, w176_5 float8, w176 float8, w175_5 float8, w175 float8, w174_5 float8, w174 float8, w173_5 float8, w173 float8, w172_5 float8, w172 float8, w171_5 float8, w171 float8, w170_5 float8, w170 float8, w169_5 float8, w169 float8, w168_5 float8, w168 float8, w167_5 float8, w167 float8, w166_5 float8, w166 float8, w165_5 float8, w165 float8, w164_5 float8, w164 float8, w163_5 float8, w163 float8, w162_5 float8, w162 float8, w161_5 float8, w161 float8, w160_5 float8, w160 float8, w159_5 float8, w159 float8, w158_5 float8, w158 float8, w157_5 float8, w157 float8, w156_5 float8, w156 float8, w155_5 float8, w155 float8, w154_5 float8, w154 float8, w153_5 float8, w153 float8, w152_5 float8, w152 float8, w151_5 float8, w151 float8, w150_5 float8, w150 float8, w149_5 float8, w149 float8, w148_5 float8, w148 float8, w147_5 float8, w147 float8, w146_5 float8, w146 float8, w145_5 float8, w145 float8, w144_5 float8, w144 float8, w143_5 float8, w143 float8, w142_5 float8, w142 float8, w141_5 float8, w141 float8, w140_5 float8, w140 float8, w139_5 float8, w139 float8, w138_5 float8, w138 float8, w137_5 float8, w137 float8, w136_5 float8, w136 float8, w135_5 float8, w135 float8, w134_5 float8, w134 float8, w133_5 float8, w133 float8, w132_5 float8, w132 float8, w131_5 float8, w131 float8, w130_5 float8, w130 float8, w129_5 float8, w129 float8, w128_5 float8, w128 float8, w127_5 float8, w127 float8, w126_5 float8, w126 float8, w125_5 float8, w125 float8, w124_5 float8, w124 float8, w123_5 float8, w123 float8, w122_5 float8, w122 float8, w121_5 float8, w121 float8, w120_5 float8, w120 float8, w119_5 float8, w119 float8, w118_5 float8, w118 float8, w117_5 float8, w117 float8, w116_5 float8, w116 float8, w115_5 float8, w115 float8, w114_5 float8, w114 float8, w113_5 float8, w113 float8, w112_5 float8, w112 float8, w111_5 float8, w111 float8, w110_5 float8, w110 float8, w109_5 float8, w109 float8, w108_5 float8, w108 float8, w107_5 float8, w107 float8, w106_5 float8, w106 float8, w105_5 float8, w105 float8, w104_5 float8, w104 float8, w103_5 float8, w103 float8, w102_5 float8, w102 float8, w101_5 float8, w101 float8, w100_5 float8, w100 float8, w99_5 float8, w99 float8, w98_5 float8, w98 float8, w97_5 float8, w97 float8, w96_5 float8, w96 float8, w95_5 float8, w95 float8, w94_5 float8, w94 float8, w93_5 float8, w93 float8, w92_5 float8, w92 float8, w91_5 float8, w91 float8, w90_5 float8, w90 float8, w89_5 float8, w89 float8, w88_5 float8, w88 float8, w87_5 float8, w87 float8, w86_5 float8, w86 float8, w85_5 float8, w85 float8, w84_5 float8, w84 float8, w83_5 float8, w83 float8, w82_5 float8, w82 float8, w81_5 float8, w81 float8, w80_5 float8, w80 float8, w79_5 float8, w79 float8, w78_5 float8, w78 float8, w77_5 float8, w77 float8, w76_5 float8, w76 float8, w75_5 float8, w75 float8, w74_5 float8, w74 float8, w73_5 float8, w73 float8, w72_5 float8, w72 float8, w71_5 float8, w71 float8, w70_5 float8, w70 float8, w69_5 float8, w69 float8, w68_5 float8, w68 float8, w67_5 float8, w67 float8, w66_5 float8, w66 float8, w65_5 float8, w65 float8, w64_5 float8, w64 float8, w63_5 float8, w63 float8, w62_5 float8, w62 float8, w61_5 float8, w61 float8, w60_5 float8, w60 float8, w59_5 float8, w59 float8, w58_5 float8, w58 float8, w57_5 float8, w57 float8, w56_5 float8, w56 float8, w55_5 float8, w55 float8, w54_5 float8, w54 float8, w53_5 float8, w53 float8, w52_5 float8, w52 float8, w51_5 float8, w51 float8, w50_5 float8, w50 float8, w49_5 float8, w49 float8, w48_5 float8, w48 float8, w47_5 float8, w47 float8, w46_5 float8, w46 float8, w45_5 float8, w45 float8, w44_5 float8, w44 float8, w43_5 float8, w43 float8, w42_5 float8, w42 float8, w41_5 float8, w41 float8, w40_5 float8, w40 float8, w39_5 float8, w39 float8, w38_5 float8, w38 float8, w37_5 float8, w37 float8, w36_5 float8, w36 float8, w35_5 float8, w35 float8, w34_5 float8, w34 float8, w33_5 float8, w33 float8, w32_5 float8, w32 float8, w31_5 float8, w31 float8, w30_5 float8, w30 float8, w29_5 float8, w29 float8, w28_5 float8, w28 float8, w27_5 float8, w27 float8, w26_5 float8, w26 float8, w25_5 float8, w25 float8, w24_5 float8, w24 float8, w23_5 float8, w23 float8, w22_5 float8, w22 float8, w21_5 float8, w21 float8, w20_5 float8, w20 float8, w19_5 float8, w19 float8, w18_5 float8, w18 float8, w17_5 float8, w17 float8, w16_5 float8, w16 float8, w15_5 float8, w15 float8, w14_5 float8, w14 float8, w13_5 float8, w13 float8, w12_5 float8, w12 float8, w11_5 float8, w11 float8, w10_5 float8, w10 float8, w9_5 float8, w9 float8, w8_5 float8, w8 float8, w7_5 float8, w7 float8, w6_5 float8, w6 float8, w5_5 float8, w5 float8, w4_5 float8, w4 float8, w3_5 float8, w3 float8, w2_5 float8, w2 float8, w1_5 float8, w1 float8, w0_5 float8, xlng0 float8, e0_5 float8, e1 float8, e1_5 float8, e2 float8, e2_5 float8, e3 float8, e3_5 float8, e4 float8, e4_5 float8, e5 float8, e5_5 float8, e6 float8, e6_5 float8, e7 float8, e7_5 float8, e8 float8, e8_5 float8, e9 float8, e9_5 float8, e10 float8, e10_5 float8, e11 float8, e11_5 float8, e12 float8, e12_5 float8, e13 float8, e13_5 float8, e14 float8, e14_5 float8, e15 float8, e15_5 float8, e16 float8, e16_5 float8, e17 float8, e17_5 float8, e18 float8, e18_5 float8, e19 float8, e19_5 float8, e20 float8, e20_5 float8, e21 float8, e21_5 float8, e22 float8, e22_5 float8, e23 float8, e23_5 float8, e24 float8, e24_5 float8, e25 float8, e25_5 float8, e26 float8, e26_5 float8, e27 float8, e27_5 float8, e28 float8, e28_5 float8, e29 float8, e29_5 float8, e30 float8, e30_5 float8, e31 float8, e31_5 float8, e32 float8, e32_5 float8, e33 float8, e33_5 float8, e34 float8, e34_5 float8, e35 float8, e35_5 float8, e36 float8, e36_5 float8, e37 float8, e37_5 float8, e38 float8, e38_5 float8, e39 float8, e39_5 float8, e40 float8, e40_5 float8, e41 float8, e41_5 float8, e42 float8, e42_5 float8, e43 float8, e43_5 float8, e44 float8, e44_5 float8, e45 float8, e45_5 float8, e46 float8, e46_5 float8, e47 float8, e47_5 float8, e48 float8, e48_5 float8, e49 float8, e49_5 float8, e50 float8, e50_5 float8, e51 float8, e51_5 float8, e52 float8, e52_5 float8, e53 float8, e53_5 float8, e54 float8, e54_5 float8, e55 float8, e55_5 float8, e56 float8, e56_5 float8, e57 float8, e57_5 float8, e58 float8, e58_5 float8, e59 float8, e59_5 float8, e60 float8, e60_5 float8, e61 float8, e61_5 float8, e62 float8, e62_5 float8, e63 float8, e63_5 float8, e64 float8, e64_5 float8, e65 float8, e65_5 float8, e66 float8, e66_5 float8, e67 float8, e67_5 float8, e68 float8, e68_5 float8, e69 float8, e69_5 float8, e70 float8, e70_5 float8, e71 float8, e71_5 float8, e72 float8, e72_5 float8, e73 float8, e73_5 float8, e74 float8, e74_5 float8, e75 float8, e75_5 float8, e76 float8, e76_5 float8, e77 float8, e77_5 float8, e78 float8, e78_5 float8, e79 float8, e79_5 float8, e80 float8, e80_5 float8, e81 float8, e81_5 float8, e82 float8, e82_5 float8, e83 float8, e83_5 float8, e84 float8, e84_5 float8, e85 float8, e85_5 float8, e86 float8, e86_5 float8, e87 float8, e87_5 float8, e88 float8, e88_5 float8, e89 float8, e89_5 float8, e90 float8, e90_5 float8, e91 float8, e91_5 float8, e92 float8, e92_5 float8, e93 float8, e93_5 float8, e94 float8, e94_5 float8, e95 float8, e95_5 float8, e96 float8, e96_5 float8, e97 float8, e97_5 float8, e98 float8, e98_5 float8, e99 float8, e99_5 float8, e100 float8, e100_5 float8, e101 float8, e101_5 float8, e102 float8, e102_5 float8, e103 float8, e103_5 float8, e104 float8, e104_5 float8, e105 float8, e105_5 float8, e106 float8, e106_5 float8, e107 float8, e107_5 float8, e108 float8, e108_5 float8, e109 float8, e109_5 float8, e110 float8, e110_5 float8, e111 float8, e111_5 float8, e112 float8, e112_5 float8, e113 float8, e113_5 float8, e114 float8, e114_5 float8, e115 float8, e115_5 float8, e116 float8, e116_5 float8, e117 float8, e117_5 float8, e118 float8, e118_5 float8, e119 float8, e119_5 float8, e120 float8, e120_5 float8, e121 float8, e121_5 float8, e122 float8, e122_5 float8, e123 float8, e123_5 float8, e124 float8, e124_5 float8, e125 float8, e125_5 float8, e126 float8, e126_5 float8, e127 float8, e127_5 float8, e128 float8, e128_5 float8, e129 float8, e129_5 float8, e130 float8, e130_5 float8, e131 float8, e131_5 float8, e132 float8, e132_5 float8, e133 float8, e133_5 float8, e134 float8, e134_5 float8, e135 float8, e135_5 float8, e136 float8, e136_5 float8, e137 float8, e137_5 float8, e138 float8, e138_5 float8, e139 float8, e139_5 float8, e140 float8, e140_5 float8, e141 float8, e141_5 float8, e142 float8, e142_5 float8, e143 float8, e143_5 float8, e144 float8, e144_5 float8, e145 float8, e145_5 float8, e146 float8, e146_5 float8, e147 float8, e147_5 float8, e148 float8, e148_5 float8, e149 float8, e149_5 float8, e150 float8, e150_5 float8, e151 float8, e151_5 float8, e152 float8, e152_5 float8, e153 float8, e153_5 float8, e154 float8, e154_5 float8, e155 float8, e155_5 float8, e156 float8, e156_5 float8, e157 float8, e157_5 float8, e158 float8, e158_5 float8, e159 float8, e159_5 float8, e160 float8, e160_5 float8, e161 float8, e161_5 float8, e162 float8, e162_5 float8, e163 float8, e163_5 float8, e164 float8, e164_5 float8, e165 float8, e165_5 float8, e166 float8, e166_5 float8, e167 float8, e167_5 float8, e168 float8, e168_5 float8, e169 float8, e169_5 float8, e170 float8, e170_5 float8, e171 float8, e171_5 float8, e172 float8, e172_5 float8, e173 float8, e173_5 float8, e174 float8, e174_5 float8, e175 float8, e175_5 float8, e176 float8, e176_5 float8, e177 float8, e177_5 float8, e178 float8, e178_5 float8, e179 float8, e179_5 float8);
    INSERT INTO length_year_matrix_lng_half (year) VALUES (0), (1), (2), (3), (4), (5), (6), (7), (8), (9), (10), (11), (12), (13), (14), (15), (16), (17), (18), (19), (20), (21), (22), (23), (24), (25), (26), (27), (28), (29), (30), (31), (32), (33), (34), (35), (36), (37), (38), (39), (40), (41), (42), (43), (44), (45), (46), (47), (48), (49), (50), (51), (52), (53), (54), (55), (56), (57), (58), (59), (60), (61), (62), (63), (64), (65), (66), (67), (68), (69), (70), (71), (72), (73), (74), (75), (76), (77), (78), (79), (80), (81), (82), (83), (84), (85), (86), (87), (88), (89), (90), (91), (92), (93), (94), (95), (96), (97), (98), (99), (100), (101), (102), (103), (104), (105), (106), (107), (108), (109), (110), (111), (112), (113), (114), (115), (116), (117), (118), (119), (120), (121), (122), (123), (124), (125), (126), (127), (128), (129), (130), (131), (132), (133), (134), (135), (136), (137), (138), (139), (140), (141), (142), (143), (144), (145), (146), (147), (148), (149), (150), (151), (152), (153), (154), (155), (156), (157), (158), (159), (160), (161), (162), (163), (164), (165), (166), (167), (168), (169), (170), (171), (172), (173), (174), (175), (176), (177), (178), (179), (180), (181), (182), (183), (184), (185), (186), (187), (188), (189), (190), (191), (192), (193), (194), (195), (196), (197), (198), (199), (200), (201), (202), (203), (204), (205), (206), (207), (208), (209), (210), (211), (212), (213), (214), (215), (216), (217), (218), (219), (220), (221), (222), (223), (224), (225), (226), (227), (228), (229), (230), (231), (232), (233), (234), (235), (236), (237), (238), (239), (240), (241), (242), (243), (244), (245), (246), (247), (248), (249), (250), (251), (252), (253), (254), (255), (256), (257), (258), (259), (260), (261), (262), (263), (264), (265), (266), (267), (268), (269), (270), (271), (272), (273), (274), (275), (276), (277), (278), (279), (280), (281), (282), (283), (284), (285), (286), (287), (288), (289), (290), (291), (292), (293), (294), (295), (296), (297), (298), (299), (300), (301), (302), (303), (304), (305), (306), (307), (308), (309), (310), (311), (312), (313), (314), (315), (316), (317), (318), (319), (320), (321), (322), (323), (324), (325), (326), (327), (328), (329), (330), (331), (332), (333), (334), (335), (336), (337), (338), (339), (340), (341), (342), (343), (344), (345), (346), (347), (348), (349), (350), (351), (352), (353), (354), (355), (356), (357), (358), (359), (360), (361), (362), (363), (364), (365), (366), (367), (368), (369), (370), (371), (372), (373), (374), (375), (376), (377), (378), (379), (380), (381), (382), (383), (384), (385), (386), (387), (388), (389), (390), (391), (392), (393), (394), (395), (396), (397), (398), (399), (400), (401), (402), (403), (404), (405), (406), (407), (408), (409), (410), (411), (412), (413), (414), (415), (416), (417), (418), (419), (420), (421), (422), (423), (424), (425), (426), (427), (428), (429), (430), (431), (432), (433), (434), (435), (436), (437), (438), (439), (440), (441), (442), (443), (444), (445), (446), (447), (448), (449), (450), (451), (452), (453), (454), (455), (456), (457), (458), (459), (460), (461), (462), (463), (464), (465), (466), (467), (468), (469), (470), (471), (472), (473), (474), (475), (476), (477), (478), (479), (480), (481), (482), (483), (484), (485), (486), (487), (488), (489), (490), (491), (492), (493), (494), (495), (496), (497), (498), (499), (500), (501), (502), (503), (504), (505), (506), (507), (508), (509), (510), (511), (512), (513), (514), (515), (516), (517), (518), (519), (520), (521), (522), (523), (524), (525), (526), (527), (528), (529), (530), (531), (532), (533), (534), (535), (536), (537), (538), (539), (540), (541), (542), (543), (544), (545), (546), (547), (548), (549), (550);

    DROP TABLE IF EXISTS length_year_matrix_lat_half;
    CREATE TABLE length_year_matrix_lat_half (year integer PRIMARY KEY, n89_5 float8, n89 float8, n88_5 float8, n88 float8, n87_5 float8, n87 float8, n86_5 float8, n86 float8, n85_5 float8, n85 float8, n84_5 float8, n84 float8, n83_5 float8, n83 float8, n82_5 float8, n82 float8, n81_5 float8, n81 float8, n80_5 float8, n80 float8, n79_5 float8, n79 float8, n78_5 float8, n78 float8, n77_5 float8, n77 float8, n76_5 float8, n76 float8, n75_5 float8, n75 float8, n74_5 float8, n74 float8, n73_5 float8, n73 float8, n72_5 float8, n72 float8, n71_5 float8, n71 float8, n70_5 float8, n70 float8, n69_5 float8, n69 float8, n68_5 float8, n68 float8, n67_5 float8, n67 float8, n66_5 float8, n66 float8, n65_5 float8, n65 float8, n64_5 float8, n64 float8, n63_5 float8, n63 float8, n62_5 float8, n62 float8, n61_5 float8, n61 float8, n60_5 float8, n60 float8, n59_5 float8, n59 float8, n58_5 float8, n58 float8, n57_5 float8, n57 float8, n56_5 float8, n56 float8, n55_5 float8, n55 float8, n54_5 float8, n54 float8, n53_5 float8, n53 float8, n52_5 float8, n52 float8, n51_5 float8, n51 float8, n50_5 float8, n50 float8, n49_5 float8, n49 float8, n48_5 float8, n48 float8, n47_5 float8, n47 float8, n46_5 float8, n46 float8, n45_5 float8, n45 float8, n44_5 float8, n44 float8, n43_5 float8, n43 float8, n42_5 float8, n42 float8, n41_5 float8, n41 float8, n40_5 float8, n40 float8, n39_5 float8, n39 float8, n38_5 float8, n38 float8, n37_5 float8, n37 float8, n36_5 float8, n36 float8, n35_5 float8, n35 float8, n34_5 float8, n34 float8, n33_5 float8, n33 float8, n32_5 float8, n32 float8, n31_5 float8, n31 float8, n30_5 float8, n30 float8, n29_5 float8, n29 float8, n28_5 float8, n28 float8, n27_5 float8, n27 float8, n26_5 float8, n26 float8, n25_5 float8, n25 float8, n24_5 float8, n24 float8, n23_5 float8, n23 float8, n22_5 float8, n22 float8, n21_5 float8, n21 float8, n20_5 float8, n20 float8, n19_5 float8, n19 float8, n18_5 float8, n18 float8, n17_5 float8, n17 float8, n16_5 float8, n16 float8, n15_5 float8, n15 float8, n14_5 float8, n14 float8, n13_5 float8, n13 float8, n12_5 float8, n12 float8, n11_5 float8, n11 float8, n10_5 float8, n10 float8, n9_5 float8, n9 float8, n8_5 float8, n8 float8, n7_5 float8, n7 float8, n6_5 float8, n6 float8, n5_5 float8, n5 float8, n4_5 float8, n4 float8, n3_5 float8, n3 float8, n2_5 float8, n2 float8, n1_5 float8, n1 float8, n0_5 float8, xlat0 float8, s0_5 float8, s1 float8, s1_5 float8, s2 float8, s2_5 float8, s3 float8, s3_5 float8, s4 float8, s4_5 float8, s5 float8, s5_5 float8, s6 float8, s6_5 float8, s7 float8, s7_5 float8, s8 float8, s8_5 float8, s9 float8, s9_5 float8, s10 float8, s10_5 float8, s11 float8, s11_5 float8, s12 float8, s12_5 float8, s13 float8, s13_5 float8, s14 float8, s14_5 float8, s15 float8, s15_5 float8, s16 float8, s16_5 float8, s17 float8, s17_5 float8, s18 float8, s18_5 float8, s19 float8, s19_5 float8, s20 float8, s20_5 float8, s21 float8, s21_5 float8, s22 float8, s22_5 float8, s23 float8, s23_5 float8, s24 float8, s24_5 float8, s25 float8, s25_5 float8, s26 float8, s26_5 float8, s27 float8, s27_5 float8, s28 float8, s28_5 float8, s29 float8, s29_5 float8, s30 float8, s30_5 float8, s31 float8, s31_5 float8, s32 float8, s32_5 float8, s33 float8, s33_5 float8, s34 float8, s34_5 float8, s35 float8, s35_5 float8, s36 float8, s36_5 float8, s37 float8, s37_5 float8, s38 float8, s38_5 float8, s39 float8, s39_5 float8, s40 float8, s40_5 float8, s41 float8, s41_5 float8, s42 float8, s42_5 float8, s43 float8, s43_5 float8, s44 float8, s44_5 float8, s45 float8, s45_5 float8, s46 float8, s46_5 float8, s47 float8, s47_5 float8, s48 float8, s48_5 float8, s49 float8, s49_5 float8, s50 float8, s50_5 float8, s51 float8, s51_5 float8, s52 float8, s52_5 float8, s53 float8, s53_5 float8, s54 float8, s54_5 float8, s55 float8, s55_5 float8, s56 float8, s56_5 float8, s57 float8, s57_5 float8, s58 float8, s58_5 float8, s59 float8, s59_5 float8, s60 float8, s60_5 float8, s61 float8, s61_5 float8, s62 float8, s62_5 float8, s63 float8, s63_5 float8, s64 float8, s64_5 float8, s65 float8, s65_5 float8, s66 float8, s66_5 float8, s67 float8, s67_5 float8, s68 float8, s68_5 float8, s69 float8, s69_5 float8, s70 float8, s70_5 float8, s71 float8, s71_5 float8, s72 float8, s72_5 float8, s73 float8, s73_5 float8, s74 float8, s74_5 float8, s75 float8, s75_5 float8, s76 float8, s76_5 float8, s77 float8, s77_5 float8, s78 float8, s78_5 float8, s79 float8, s79_5 float8, s80 float8, s80_5 float8, s81 float8, s81_5 float8, s82 float8, s82_5 float8, s83 float8, s83_5 float8, s84 float8, s84_5 float8, s85 float8, s85_5 float8, s86 float8, s86_5 float8, s87 float8, s87_5 float8, s88 float8, s88_5 float8, s89 float8, s89_5 float8);
    INSERT INTO length_year_matrix_lat_half (year) VALUES (0), (1), (2), (3), (4), (5), (6), (7), (8), (9), (10), (11), (12), (13), (14), (15), (16), (17), (18), (19), (20), (21), (22), (23), (24), (25), (26), (27), (28), (29), (30), (31), (32), (33), (34), (35), (36), (37), (38), (39), (40), (41), (42), (43), (44), (45), (46), (47), (48), (49), (50), (51), (52), (53), (54), (55), (56), (57), (58), (59), (60), (61), (62), (63), (64), (65), (66), (67), (68), (69), (70), (71), (72), (73), (74), (75), (76), (77), (78), (79), (80), (81), (82), (83), (84), (85), (86), (87), (88), (89), (90), (91), (92), (93), (94), (95), (96), (97), (98), (99), (100), (101), (102), (103), (104), (105), (106), (107), (108), (109), (110), (111), (112), (113), (114), (115), (116), (117), (118), (119), (120), (121), (122), (123), (124), (125), (126), (127), (128), (129), (130), (131), (132), (133), (134), (135), (136), (137), (138), (139), (140), (141), (142), (143), (144), (145), (146), (147), (148), (149), (150), (151), (152), (153), (154), (155), (156), (157), (158), (159), (160), (161), (162), (163), (164), (165), (166), (167), (168), (169), (170), (171), (172), (173), (174), (175), (176), (177), (178), (179), (180), (181), (182), (183), (184), (185), (186), (187), (188), (189), (190), (191), (192), (193), (194), (195), (196), (197), (198), (199), (200), (201), (202), (203), (204), (205), (206), (207), (208), (209), (210), (211), (212), (213), (214), (215), (216), (217), (218), (219), (220), (221), (222), (223), (224), (225), (226), (227), (228), (229), (230), (231), (232), (233), (234), (235), (236), (237), (238), (239), (240), (241), (242), (243), (244), (245), (246), (247), (248), (249), (250), (251), (252), (253), (254), (255), (256), (257), (258), (259), (260), (261), (262), (263), (264), (265), (266), (267), (268), (269), (270), (271), (272), (273), (274), (275), (276), (277), (278), (279), (280), (281), (282), (283), (284), (285), (286), (287), (288), (289), (290), (291), (292), (293), (294), (295), (296), (297), (298), (299), (300), (301), (302), (303), (304), (305), (306), (307), (308), (309), (310), (311), (312), (313), (314), (315), (316), (317), (318), (319), (320), (321), (322), (323), (324), (325), (326), (327), (328), (329), (330), (331), (332), (333), (334), (335), (336), (337), (338), (339), (340), (341), (342), (343), (344), (345), (346), (347), (348), (349), (350), (351), (352), (353), (354), (355), (356), (357), (358), (359), (360), (361), (362), (363), (364), (365), (366), (367), (368), (369), (370), (371), (372), (373), (374), (375), (376), (377), (378), (379), (380), (381), (382), (383), (384), (385), (386), (387), (388), (389), (390), (391), (392), (393), (394), (395), (396), (397), (398), (399), (400), (401), (402), (403), (404), (405), (406), (407), (408), (409), (410), (411), (412), (413), (414), (415), (416), (417), (418), (419), (420), (421), (422), (423), (424), (425), (426), (427), (428), (429), (430), (431), (432), (433), (434), (435), (436), (437), (438), (439), (440), (441), (442), (443), (444), (445), (446), (447), (448), (449), (450), (451), (452), (453), (454), (455), (456), (457), (458), (459), (460), (461), (462), (463), (464), (465), (466), (467), (468), (469), (470), (471), (472), (473), (474), (475), (476), (477), (478), (479), (480), (481), (482), (483), (484), (485), (486), (487), (488), (489), (490), (491), (492), (493), (494), (495), (496), (497), (498), (499), (500), (501), (502), (503), (504), (505), (506), (507), (508), (509), (510), (511), (512), (513), (514), (515), (516), (517), (518), (519), (520), (521), (522), (523), (524), (525), (526), (527), (528), (529), (530), (531), (532), (533), (534), (535), (536), (537), (538), (539), (540), (541), (542), (543), (544), (545), (546), (547), (548), (549), (550);
  """)
  connection.commit()
  cursor.close()
  connection.close()

  # Set the range to whatever year you want to go up to (551 is the max)
  
  for i in xrange(551):
    n = 89.5
    s = 0.5
    w = 179.5
    e = 0.5

    while w > 0:
      tasks.put(Task("lng", "w", w, i))
      w -= 0.5

    while e < 180:
      tasks.put(Task("lng", "e", e, i))
      e += 0.5

    while n > 0:
      tasks.put(Task("lat", "n", n, i))
      n -= 0.5

    while s < 90:
      tasks.put(Task("lat", "s", s, i))
      s += 0.5

    tasks.put(Task("lat", "xlat", 0.0, i))
    tasks.put(Task("lng", "xlng", 0.0, i))

  for i in range(num_processors):
    tasks.put(None)




