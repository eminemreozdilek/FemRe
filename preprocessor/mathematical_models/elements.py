import numpy as np

INV = np.linalg.inv
DET = np.linalg.det
LEN = np.linalg.norm

brick_master_points = [[-1, -1, -1],
                       [1, -1, -1],
                       [1, 1, -1],
                       [-1, 1, -1],
                       [-1, -1, 1],
                       [1, -1, 1],
                       [1, 1, 1],
                       [-1, 1, 1]]

tetra_master_points = [[0, 0, 0],
                       [1, 0, 0],
                       [0, 1, 0],
                       [0, 0, 1]]


# 3D tetrahedral bölgede tek noktalı integrasyon kuralı
def tetra_IntegrateOn3DDomainWithQuadN1(h):
    return h(0.25, 0.25, 0.25) / 6


# Tetrahedralin 4 sınır yüzeyinde tek noktalı integral alınıyor (w=1/2)
def tetra_IntegrateOn3DTriangeAreas(h):
    total = 0
    for k in range(4):
        if k == 0: r, s, t = 0, 1 / 3, 1 / 3
        if k == 1: r, s, t = 1 / 3, 0, 1 / 3
        if k == 2: r, s, t = 1 / 3, 1 / 3, 0
        if k == 3: r, s, t = 1 / 3, 1 / 3, 1 / 3
        total += 0.5 * h(r, s, t, k)
    return total


# Şekil fonksiyonları vektörü (4x1)
def tetra_SF(r, s, t):
    return np.asarray([1 - r - s - t, r, s, t])


# Şekil fonksiyonlarının türev matrisi (4x3)
def tetra_dF_dr(r, s, t):
    return np.asarray([[-1, -1, -1],
                       [1, 0, 0],
                       [0, 1, 0],
                       [0, 0, 1]])


# 3D bölgede n=2 Gauss integrasyon şeması
def brick_IntegrateOn3DDomainWithGaussN2(h):
    total = 0
    p = [-1 / 3 ** 0.5, 1 / 3 ** 0.5]
    w = [1, 1]
    for i in range(2):
        for j in range(2):
            for k in range(2):
                total += (w[i] * w[j] * w[k]) * h(p[i], p[j], p[k])
    return total


# 3D sınırlarda n=2 Gauss integrasyon şeması (k: Sınır numarası)
def brick_IntegrateOn3DBoundariesWithGaussN2(h):
    total = 0
    p = [-1 / 3 ** 0.5, 1 / 3 ** 0.5]
    w = [1, 1]
    for i in range(2):
        for j in range(2):
            rb = [-1, 1, p[i], p[i], p[i], p[i]]
            sb = [p[i], p[i], -1, 1, p[j], p[j]]
            tb = [p[j], p[j], p[j], p[j], -1, 1]
            for k in range(6):
                total += w[i] * w[j] * h(rb[k], sb[k], tb[k], k)
    return total


# Şekil fonksiyonları vektörü (8x1)
def brick_SF(r, s, t):
    return 0.125 * np.asarray([(1 + ri * r) * (1 + si * s) * (1 + ti * t)
                               for ri, si, ti in brick_master_points])


# Şekil fonksiyonlarının türev matrisi (8x3)
def brick_dF_dr(r, s, t):
    return 0.125 * np.asarray([[(ri) * (1 + si * s) * (1 + ti * t),
                                (1 + ri * r) * (si) * (1 + ti * t),
                                (1 + ri * r) * (1 + si * s) * (ti)]
                               for ri, si, ti in brick_master_points])


class BrickElement:
    def __init__(elm, id, conn, material):
        elm.id = id
        elm.conn = conn  # Bağlantı haritası [DN1 ... DN8]
        elm.E, elm.p, elm.alpha = material.youngs_modulus, material.poissons_ratio, material.thermal_expansion_coefficent
        elm.boundaryForceX = [0] * 6  # Sınır-Yüzey X [q1x, q2x, q3x, q4x, q5x, q6x]
        elm.boundaryForceY = [0] * 6  # Sınır-Yüzey Y [q1y, q2y, q3y, q4y, q5y, q6y]
        elm.boundaryForceZ = [0] * 6  # Sınır-Yüzey Z [q1z, q2z, q3z, q4z, q5z, q6z]
        elm.volumeForce = [0] * 3  # Hacim Kuvvetleri [bx, by, bz]
        elm.temperatureChange = 0  # Uniform sıcaklık değişimi (delta_T)

    def __str__(self):
        nodes = ""
        for node in self.conn:
            nodes = nodes + str(node.id) + ", "
        return "Element BrickEight - " + str(self.id) + " between nodes: " + nodes[:-2]

    def __repr__(self):
        return str(self)

    def save_element_to_dataframe(self, element_storage):
        element_storage.loc[self.id] = {"ElementID": self.id,
                                        "Element": self, }
        return element_storage

    # Kod-Vektörü [u1 ... u8, v1 ... v8, w1 ... w8]
    def code(elm):
        return [n.code[0] for n in elm.conn] + \
            [n.code[1] for n in elm.conn] + \
            [n.code[2] for n in elm.conn]

    # Nodal koordinat matrisi (3x8)
    def XM(elm):
        n1, n2, n3, n4, n5, n6, n7, n8 = elm.conn
        return np.asarray([[n1.X, n2.X, n3.X, n4.X, n5.X, n6.X, n7.X, n8.X],
                           [n1.Y, n2.Y, n3.Y, n4.Y, n5.Y, n6.Y, n7.Y, n8.Y],
                           [n1.Z, n2.Z, n3.Z, n4.Z, n5.Z, n6.Z, n7.Z, n8.Z]])

    # Jacobian Matrisi
    def JM(elm, r, s, t):
        return elm.XM() @ brick_dF_dr(r, s, t)

    # Jacobian (Det(JM))
    def detJM(elm, r, s, t):
        return abs(DET(elm.JM(r, s, t)))

    # Şekil fonksiyonlarının gerçek koordinatlara göre türev matrisi
    def dF_DX(elm, r, s, t):
        return brick_dF_dr(r, s, t) @ INV(elm.JM(r, s, t))

    # Genleme-yer değiştirme matrisi (6x24)
    def BM(elm, r, s, t):
        dF_dX = elm.dF_DX(r, s, t)
        B = np.zeros((6, 24))
        B[0, 0:8] = dF_dX[:, 0]
        B[1, 8:16] = dF_dX[:, 1]
        B[2, 16:24] = dF_dX[:, 2]
        B[3, 8:16] = dF_dX[:, 2]
        B[3, 16:24] = dF_dX[:, 1]
        B[4, 0:8] = dF_dX[:, 2]
        B[4, 16:24] = dF_dX[:, 0]
        B[5, 0:8] = dF_dX[:, 1]
        B[5, 8:16] = dF_dX[:, 0]
        return B

    # Bünye (malzeme) matrisi [C] (6x6)
    def C(elm):
        E, p = elm.E, elm.p
        return E / ((1 + p) * (1 - 2 * p)) * \
            np.asarray([[1 - p, p, p, 0, 0, 0],
                        [p, 1 - p, p, 0, 0, 0],
                        [p, p, 1 - p, 0, 0, 0],
                        [0, 0, 0, 0.5 - p, 0, 0],
                        [0, 0, 0, 0, 0.5 - p, 0],
                        [0, 0, 0, 0, 0, 0.5 - p]])

    # Rijitlik Matrisi [K] (24x24)
    def K(elm):
        def dK(r, s, t):  # Rijitlik Matrisi integrandı
            C = elm.C()
            B = elm.BM(r, s, t)
            J = elm.detJM(r, s, t)
            return B.T @ C @ B * J

        return brick_IntegrateOn3DDomainWithGaussN2(dK)

    # Eleman hacim-kuvvetleri vektörü (24x1)
    def B(elm):
        def dB(r, s, t):  # Vetörün integrandı
            bx, by, bz = elm.volumeForce
            if bx == 0 and by == 0 and bz == 0: return np.zeros(24)
            J = elm.detJM(r, s, t)
            SFV = brick_SF(r, s, t)
            SF24 = np.concatenate((SFV, SFV, SFV))
            return J * SF24 * ([bx] * 8 + [by] * 8 + [bz] * 8)

        return brick_IntegrateOn3DDomainWithGaussN2(dB)

    # Eleman sınır-yüzey dış yükleri vektörü (24x1)
    def S(elm):
        def dS(r, s, t, k):  # Vetörün integrandı
            qx = elm.boundaryForceX[k]
            qy = elm.boundaryForceY[k]
            qz = elm.boundaryForceZ[k]
            if qx == 0 and qy == 0 and qz == 0: return np.zeros(24)
            SFV = brick_SF(r, s, t)
            JM = elm.JM(r, s, t)
            J = 0
            if k in [0, 1]: J = ((JM[0, 2] * JM[1, 1] - JM[0, 1] * JM[1, 2]) ** 2 +
                                 (JM[0, 2] * JM[2, 1] - JM[0, 1] * JM[2, 2]) ** 2 +
                                 (JM[1, 2] * JM[2, 1] - JM[1, 1] * JM[2, 2]) ** 2) ** 0.5
            if k in [2, 3]: J = ((JM[0, 2] * JM[1, 0] - JM[0, 0] * JM[1, 2]) ** 2 +
                                 (JM[0, 2] * JM[2, 0] - JM[0, 0] * JM[2, 2]) ** 2 +
                                 (JM[1, 2] * JM[2, 0] - JM[1, 0] * JM[2, 2]) ** 2) ** 0.5
            if k in [4, 5]: J = ((JM[0, 1] * JM[1, 0] - JM[0, 0] * JM[1, 1]) ** 2 +
                                 (JM[0, 1] * JM[2, 0] - JM[0, 0] * JM[2, 1]) ** 2 +
                                 (JM[1, 1] * JM[2, 0] - JM[1, 0] * JM[2, 1]) ** 2) ** 0.5
            return J * np.concatenate((SFV * qx, SFV * qy, SFV * qz))

        return brick_IntegrateOn3DBoundariesWithGaussN2(dS)

    # Eleman sıcaklık değişimi vektörü (24x1)
    def T(elm):
        def dT(r, s, t):  # Vetörün integrandı
            alpha = elm.alpha
            deltaT = elm.temperatureChange
            if alpha == 0 or deltaT == 0: return np.zeros(24)
            ALPHA = np.asarray([alpha, alpha, alpha, 0, 0, 0])
            C = elm.C()
            B = elm.BM(r, s, t)
            J = elm.detJM(r, s, t)
            return B.T @ C @ ALPHA * deltaT * J

        return brick_IntegrateOn3DDomainWithGaussN2(dT)

    # solver a gönderilecek olan rijitlik matrisi
    def StiffnessMatrixToContribute(elm):
        return elm.K()

    # solver a gönderilecek olan sağ taraf (RHS)
    def RHSVectorsToContribute(self):
        return self.B() + self.S() + self.T()

    # Hesaplanmış olan sistem serbestliklerini (yer-değiştirmeleri) alıp
    # içinden ilgili elemana ait olanları ayırır ve elm.U da saklar
    def set_solution(self, US):
        code = self.code()
        self.U = US[code]

    # Gerilme vektörü
    def SigmaVec(self, r, s, t):
        U = self.U
        C = self.C()
        BM = self.BM(r, s, t)
        alpha = self.alpha
        deltaT = self.temperatureChange
        ALPHA = np.asarray([alpha, alpha, alpha, 0, 0, 0])
        return C @ (BM @ U - ALPHA * deltaT)

    # verilen nodal değerleri nodlara paslar
    def appendNodeValues(self, nodal_values):
        for i, node in enumerate(self.conn):
            node.values.append(nodal_values[i])

    def stress_array(self):
        return np.mean(np.array([self.SigmaVec(ri, si, ti)
                                 for ri, si, ti in tetra_master_points]).transpose(), axis=1)

    def strain_array(self):
        return np.mean(np.array([self.StrainVec(ri, si, ti)
                                 for ri, si, ti in tetra_master_points]).transpose(), axis=1)

    def von_misses_stress(self):
        stress = self.stress_array()
        return np.sqrt(
            stress[0] ** 2 + stress[1] ** 2 + stress[2] ** 2 - stress[0] * stress[1] - stress[1] * stress[2] - stress[
                2] * stress[0] + 3 * (stress[3] ** 2 + stress[4] ** 2 + stress[5] ** 2))

    def von_misses_strain(self):
        strain = self.strain_array()
        return np.sqrt(2 / 3 * (
                strain[0] ** 2 + strain[1] ** 2 + strain[2] ** 2 - strain[0] * strain[1] - strain[1] * strain[2] -
                strain[2] * strain[0] +
                3 * (strain[3] ** 2 + strain[4] ** 2 + strain[5] ** 2)))

    def von_misses_energy(self):
        return self.von_misses_strain() * self.von_misses_stress() / 2

    def SigmaXAverage(self):
        return [node.mean_value()
                for node in self.conn]


class TetraElement:
    def __init__(elm, id, conn, material):
        elm.id = id
        elm.conn = conn
        elm.E, elm.p, elm.alpha = material.youngs_modulus, material.poissons_ratio, material.thermal_expansion_coefficent
        elm.boundaryForceX = [0] * 4  # Sınır-Yüzey X [q1x, q2x, q3x, q4x]
        elm.boundaryForceY = [0] * 4  # Sınır-Yüzey Y [q1y, q2y, q3y, q4y]
        elm.boundaryForceZ = [0] * 4  # Sınır-Yüzey Z [q1z, q2z, q3z, q4z]
        elm.volumeForce = [0] * 3  # Hacim Kuvvetleri [bx, by, bz]
        elm.temperatureChange = 0  # Uniform sıcaklık değişimi (delta_T)

    def __int__(self):
        return self.id

    def __str__(self):
        nodes = ""
        for node in self.conn:
            nodes = nodes + str(node.id) + ", "
        return "Element TetraFour - " + str(self.id) + " between nodes: " + nodes[:-2]

    def __repr__(self):
        return str(self)

    def save_element_to_dataframe(self, element_storage):
        element_storage.loc[self.id] = {"ElementID": self.id,
                                        "Element": self, }
        return element_storage

    # Kod-Vektörü [u1 ... u4, v1 ... v4, w1 ... w4]
    def code(elm):
        return [n.code[0] for n in elm.conn] + \
            [n.code[1] for n in elm.conn] + \
            [n.code[2] for n in elm.conn]

    # Nodal koordinat matrisi (3x4)
    def XM(elm):
        n1, n2, n3, n4 = elm.conn
        return np.asarray([[n1.X, n2.X, n3.X, n4.X],
                           [n1.Y, n2.Y, n3.Y, n4.Y],
                           [n1.Z, n2.Z, n3.Z, n4.Z]])

    # Jacobian Matrisi
    def JM(elm, r, s, t):
        return elm.XM() @ tetra_dF_dr(r, s, t)

    # Jacobian (Det(JM))
    def detJM(elm, r, s, t):
        return abs(DET(elm.JM(r, s, t)))

    # Şekil fonksiyonlarının gerçek koordinatlara göre türev matrisi
    def dF_DX(elm, r, s, t):
        return tetra_dF_dr(r, s, t) @ INV(elm.JM(r, s, t))

    # Genleme-yer değiştirme matrisi (6x12)
    def BM(elm, r, s, t):
        dF_dX = elm.dF_DX(r, s, t)
        B = np.zeros((6, 12))
        B[0, 0:4] = dF_dX[:, 0]
        B[1, 4:8] = dF_dX[:, 1]
        B[2, 8:12] = dF_dX[:, 2]
        B[3, 4:8] = dF_dX[:, 2]
        B[3, 8:12] = dF_dX[:, 1]
        B[4, 0:4] = dF_dX[:, 2]
        B[4, 8:12] = dF_dX[:, 0]
        B[5, 0:4] = dF_dX[:, 1]
        B[5, 4:8] = dF_dX[:, 0]
        return B

    # Bünye (malzeme) matrisi [C] (6x6)
    def C(elm):
        E, p = elm.E, elm.p
        return E / ((1 + p) * (1 - 2 * p)) * \
            np.asarray([[1 - p, p, p, 0, 0, 0],
                        [p, 1 - p, p, 0, 0, 0],
                        [p, p, 1 - p, 0, 0, 0],
                        [0, 0, 0, 0.5 - p, 0, 0],
                        [0, 0, 0, 0, 0.5 - p, 0],
                        [0, 0, 0, 0, 0, 0.5 - p]])

    # Rijitlik Matrisi [K] (12x12)
    def K(elm):
        def dK(r, s, t):  # Rijitlik Matrisi integrandı
            C = elm.C()
            B = elm.BM(r, s, t)
            J = elm.detJM(r, s, t)
            return B.T @ C @ B * J

        return tetra_IntegrateOn3DDomainWithQuadN1(dK)

    # Eleman hacim-kuvvetleri vektörü (12x1)
    def B(elm):
        def dB(r, s, t):  # Vetörün integrandı
            bx, by, bz = elm.volumeForce
            if bx == 0 and by == 0 and bz == 0: return np.zeros(12)
            J = elm.detJM(r, s, t)
            SFV = tetra_SF(r, s, t)
            SF12 = np.concatenate((SFV, SFV, SFV))
            return J * SF12 * ([bx] * 4 + [by] * 4 + [bz] * 4)

        return tetra_IntegrateOn3DDomainWithQuadN1(dB)

    # Eleman sınır-yüzey dış yükleri vektörü (12x1)
    def S(elm):
        def dS(r, s, t, k):  # Vetörün integrandı
            qx = elm.boundaryForceX[k]
            qy = elm.boundaryForceY[k]
            qz = elm.boundaryForceZ[k]
            if qx == 0 and qy == 0 and qz == 0: return np.zeros(12)
            SFV = tetra_SF(r, s, t)
            surfaceMap = [[1, 3, 4], [1, 4, 2], [1, 2, 3], [2, 3, 4]]
            XM = elm.XM()
            Xa = XM[:, surfaceMap[k][0] - 1]
            Xb = XM[:, surfaceMap[k][1] - 1]
            Xc = XM[:, surfaceMap[k][2] - 1]
            J = LEN(np.cross(Xb - Xa, Xc - Xa))
            return J * np.concatenate((SFV * qx, SFV * qy, SFV * qz))

        return tetra_IntegrateOn3DTriangeAreas(dS)

    # Eleman sıcaklık değişimi vektörü (12x1)
    def T(elm):
        def dT(r, s, t):  # Vetörün integrandı
            alpha = elm.alpha
            deltaT = elm.temperatureChange
            if alpha == 0 or deltaT == 0: return np.zeros(12)
            ALPHA = np.asarray([alpha, alpha, alpha, 0, 0, 0])
            C = elm.C()
            B = elm.BM(r, s, t)
            J = elm.detJM(r, s, t)
            return B.T @ C @ ALPHA * deltaT * J

        return tetra_IntegrateOn3DDomainWithQuadN1(dT)

    # solver a gönderilecek olan rijitlik matrisi
    def StiffnessMatrixToContribute(elm):
        return elm.K()

    # solver a gönderilecek olan sağ taraf (RHS)
    def RHSVectorsToContribute(elm):
        return elm.B() + elm.S() + elm.T()

    # Hesaplanmış olan sistem serbestliklerini (yer-değiştirmeleri) alıp
    # içinden ilgili elemana ait olanları ayırır ve elm.U da saklar
    def set_solution(self, US):
        code = self.code()
        self.U = US[code]

    # Gerilme vektörü
    def SigmaVec(self, r, s, t):
        U = self.U
        C = self.C()
        BM = self.BM(r, s, t)
        alpha = self.alpha
        deltaT = self.temperatureChange
        ALPHA = np.asarray([alpha, alpha, alpha, 0, 0, 0])
        return C @ (BM @ U - ALPHA * deltaT)

    def StrainVec(self, r, s, t):
        U = self.U
        BM = self.BM(r, s, t)
        return BM @ U

    # verilen nodal değerleri nodlara paslar
    def appendNodeValues(self, nodal_values):
        for i, node in enumerate(self.conn):
            node.values.append(nodal_values[i])

    def stress_array(self):
        return np.mean(np.array([self.SigmaVec(ri, si, ti)
                                 for ri, si, ti in tetra_master_points]).transpose(), axis=1)

    def strain_array(self):
        return np.mean(np.array([self.StrainVec(ri, si, ti)
                                 for ri, si, ti in tetra_master_points]).transpose(), axis=1)

    def von_misses_stress(self):
        stress = self.stress_array()
        return np.sqrt(
            stress[0] ** 2 + stress[1] ** 2 + stress[2] ** 2 - stress[0] * stress[1] - stress[1] * stress[2] - stress[
                2] * stress[0] + 3 * (stress[3] ** 2 + stress[4] ** 2 + stress[5] ** 2))

    def von_misses_strain(self):
        strain = self.strain_array()
        return np.sqrt(2 / 3 * (
                strain[0] ** 2 + strain[1] ** 2 + strain[2] ** 2 - strain[0] * strain[1] - strain[1] * strain[2] -
                strain[2] * strain[0] +
                3 * (strain[3] ** 2 + strain[4] ** 2 + strain[5] ** 2)))

    def von_misses_energy(self):
        return self.von_misses_strain() * self.von_misses_stress() / 2

    def SigmaXAverage(self):
        return [node.mean_value()
                for node in self.conn]
