"""Access to the GUI/CLI via 'python -m surgeo' (with or without args)"""
from surgeo.app.common_entry import SurgeoCommonEntry


entry = SurgeoCommonEntry()
entry.main()
