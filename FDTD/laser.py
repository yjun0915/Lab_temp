import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# 격자 크기 및 시뮬레이션 파라미터
Nx, Ny = 200, 200  # 격자 크기
dx = dy = 1e-6  # 격자 간격 (1 μm)
dt = dx / (3e8 * np.sqrt(2))  # Courant 조건을 고려한 시간 스텝
Tmax = 300  # 시뮬레이션 스텝 수

# 전자기장 초기화
Ez = np.zeros((Nx, Ny))  # 전계 Ez
Hx = np.zeros((Nx, Ny))  # 자계 Hx
Hy = np.zeros((Nx, Ny))  # 자계 Hy

# 소스 설정 (가우시안 펄스)
x_src, y_src = Nx // 2, Ny // 2  # 소스 위치 (중앙)


def gaussian_pulse(t, t0=50, spread=15):
    return np.exp(-((t - t0) / spread) ** 2)


# 애니메이션을 위한 리스트
frames = []

# FDTD 루프
for t in range(Tmax):
    # Hx 업데이트 (Faraday 방정식)
    Hx[:-1, :] -= (dt / (dx * 4 * np.pi * 1e-7)) * (Ez[1:, :] - Ez[:-1, :])

    # Hy 업데이트
    Hy[:, :-1] += (dt / (dx * 4 * np.pi * 1e-7)) * (Ez[:, 1:] - Ez[:, :-1])

    # Ez 업데이트 (Ampère 방정식)
    Ez[1:, 1:] += (dt / (dx * 8.85e-12)) * (
            (Hy[1:, 1:] - Hy[:-1, 1:]) - (Hx[1:, 1:] - Hx[1:, :-1])
    )

    # 소스 적용 (가우시안 펄스)
    Ez[x_src, y_src] += gaussian_pulse(t)

    # 시각화를 위한 데이터 저장
    if t % 5 == 0:
        frames.append(Ez.copy())

# 애니메이션 생성
fig, ax = plt.subplots()
im = ax.imshow(frames[0], cmap="RdBu", interpolation="bilinear", vmin=-0.1, vmax=0.1)


def update(frame):
    im.set_array(frame)
    return [im]


ani = animation.FuncAnimation(fig, update, frames=frames, interval=50, blit=True)
plt.show()
