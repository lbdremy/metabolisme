// Les contrats de preuve vivent dans le package partagé (les outils qui
// génèrent le contenu les utilisent aussi) ; l'app les ré-exporte pour
// garder une seule porte d'entrée « contracts/ ».
export * from "@metabolisme/evidence";
