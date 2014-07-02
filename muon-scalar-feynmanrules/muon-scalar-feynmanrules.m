(* ::Package:: *)


$FeynRulesPath = SetDirectory[
    "~/Library/Mathematica/Applications/feynrules-2.1"]; 
<< "FeynRules`"


ResetDirectory[]
LoadModel["muon-scalar-feynmanrules/SM.fr", "muon-scalar-feynmanrules/muon-scalar.fr"]; 


\[ScriptCapitalL]new = (1/2)*del[phi, \[Mu]]*del[phi, \[Mu]] - (Mphi^2/2)*phi^2 + 
   gsm*mubar . mu*phi + gse*ebar . e*phi


vertices = FeynmanRules[\[ScriptCapitalL]new]


decays = ComputeWidths[vertices]


UpdateWidths[decays]


CheckHermiticity[LSM + \[ScriptCapitalL]new]


WriteUFO[LSM + \[ScriptCapitalL]new]



