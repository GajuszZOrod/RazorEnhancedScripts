for i in range(10):
    macroName = 'LukmistrzZlecenia.py'
    Misc.ScriptRun(macroName)
    while Misc.ScriptStatus(macroName):
        Misc.NoOperation()