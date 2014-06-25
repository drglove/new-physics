(* ::Package:: *)

Directory[]


$FeynRulesPath = SetDirectory[
    "~/Library/Mathematica/Applications/feynrules-2.1"]; 
<< "FeynRules`"


SetDirectory[NotebookDirectory[]];
LoadModel["SM.fr", "muon-scalar.fr"]; 


\[ScriptCapitalL]new = (1/2)*del[phi, \[Mu]]*del[phi, \[Mu]] - (Mphi^2/2)*phi^2 + 
   gsm*mubar . mu*phi + gse*ebar . e*phi


vertices = FeynmanRules[\[ScriptCapitalL]new]


decays=ComputeWidths[vertices]


(* ::Output:: *)
(*(gse^2 (-2 Me+Mphi) (2 Me+Mphi) Sqrt[Mphi^2 (-4 Me^2+Mphi^2)])/(8 \[Pi] Abs[Mphi]^3)*)


(* ::Input:: *)
(*UpdateWidths[decays]*)


CheckHermiticity[LSM + \[ScriptCapitalL]new]


WriteUFO[LSM + \[ScriptCapitalL]new]



