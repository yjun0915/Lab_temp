debug = False

class Function:
    def __init__(self, _stages):
        self.stages = _stages

    def status(self):
        val = [state.get_status(channel=1) for state in self.stages.loc[0]]
        if debug: print("[Status]: ", val)
        return val

    def is_stable(self):
        arr = self.status()
        var = [True for _ in range(len(arr))]
        keys = ["moving_fw", "moving_bk"]
        for _ in range(len(arr)):
            for item in arr[_]:
                for key in keys:
                    if item == key:
                        var[_] = False
        if debug: print("[Is Stable]: ", var)
        return var
