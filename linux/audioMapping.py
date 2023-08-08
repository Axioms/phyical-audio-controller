mapping = {
100: 1.0,
99: 0.970315,
98: 0.941224,
97: 0.91272,
96: 0.884797,
95: 0.857449,
94: 0.830671,
93: 0.804457,
92: 0.7788,
91: 0.753694,
90: 0.729133,
89: 0.705113,
88: 0.681625,
87: 0.658665,
86: 0.636227,
85: 0.614304,
84: 0.59289,
83: 0.57198,
82: 0.551567,
81: 0.531646,
80: 0.512211,
79: 0.493255,
78: 0.474773,
77: 0.456758,
76: 0.439204,
75: 0.422107,
74: 0.405459,
73: 0.389254,
72: 0.373487,
71: 0.358152,
70: 0.343242,
69: 0.328752,
68: 0.314676,
67: 0.301007,
66: 0.28774,
65: 0.274869,
64: 0.262387,
63: 0.250289,
62: 0.238569,
61: 0.22722,
60: 0.216237,
59: 0.205614,
58: 0.195345,
57: 0.185423,
56: 0.175843,
55: 0.166599,
54: 0.157685,
53: 0.149095,
52: 0.140822,
51: 0.132861,
50: 0.125206,
49: 0.117851,
48: 0.11079,
47: 0.104016,
46: 0.097524,
45: 0.091309,
44: 0.085363,
43: 0.079681,
42: 0.074257,
41: 0.069085,
40: 0.064158,
39: 0.059472,
38: 0.05502,
37: 0.050795,
36: 0.046793,
35: 0.043006,
34: 0.03943,
33: 0.036057,
32: 0.032883,
31: 0.0299,
30: 0.027104,
29: 0.024488,
28: 0.022045,
27: 0.019771,
26: 0.017659,
25: 0.015702,
24: 0.013896,
23: 0.012234,
22: 0.01071,
21: 0.009319,
20: 0.008053,
19: 0.006907,
18: 0.005876,
17: 0.004953,
16: 0.004132,
15: 0.003407,
14: 0.002772,
13: 0.002221,
12: 0.001749,
11: 0.001349,
10: 0.001015,
9: 0.000741,
8: 0.000522,
7: 0.000351,
6: 0.000222,
5: 0.000129,
4: 6.7e-05,
3: 2.8e-05,
2: 9e-06,
1: 1e-06,
0: 0.0
}

def GetFloatValue(value: int) -> float:
    return 0.000001003 * pow(value, 3)

def GetIntVlaue(value: float) -> int:
    return round(pow((value / 0.000001003), 1/3))