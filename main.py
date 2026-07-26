#Pydroid run kivy

from pathlib import Path

from app_kivy import ZaTransportApp
from logistics_engine import LogisticsEngine


def find_workbook() -> Path:
    project_folder = Path(__file__).resolve().parent

    possible_paths = [
        project_folder / "data" / "ZaTransport Warehouse.xlsx",
        project_folder / "ZaTransport Warehouse.xlsx",
    ]

    for workbook_path in possible_paths:
        if workbook_path.exists():
            print(f"Found workbook:\n{workbook_path}")
            return workbook_path

    checked = "\n".join(str(p) for p in possible_paths)

    raise FileNotFoundError(
        "ZaTransport Warehouse.xlsx was not found.\n\n"
        f"Checked:\n{checked}"
    )



def main():
    workbook_path = find_workbook()

    print(
        f"Loading workbook:\n{workbook_path}",
        flush=True
    )

    engine = LogisticsEngine(
        str(workbook_path)
    )

    loaded = engine.load()

    if loaded is False:
        raise RuntimeError(
            "The workbook was found, but the "
            "logistics engine could not load it."
        )

    ZaTransportApp(engine).run()


if __name__ == "__main__":
    try:
        main()

    except Exception as error:
        print(
            "\nUnable to start ZaTransport Logistics Engine:\n"
            f"{type(error).__name__}: {error}",
            flush=True
        )