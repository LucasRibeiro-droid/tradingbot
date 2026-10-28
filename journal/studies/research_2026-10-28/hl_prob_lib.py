def Ff(z, side):
    pos = z.pos if side == "up" else 1 - z.pos
    dist = np.log(z.h / z.c) if side == "up" else np.log(z.c / z.l)
    g = z.gap if side == "up" else -z.gap
    return np.column_stack([np.ones(len(z)), z.left, z.so_far, pos, dist / z.rng_hat, g * 100, z.so_far * z.left, pos * z.left])
def fit(X, y, it=50):
    w = np.zeros(X.shape[1])
    for _ in range(it):
        p = 1 / (1 + np.exp(-X @ w)); W = p * (1 - p) + 1e-9
        w += np.linalg.solve((X.T * W) @ X + 1e-6 * np.eye(len(w)), X.T @ (y - p))
    return w
def auc(p, y):
    o = np.argsort(p); r = np.empty(len(p)); r[o] = np.arange(1, len(p) + 1)
    n1 = y.sum(); n0 = len(y) - n1
    return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)
