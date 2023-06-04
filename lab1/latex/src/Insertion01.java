public class Insertion {	

	public static void main(String[] args) {
		int[] lista = {5, 2, 4, 6, 1, 3};
		imprimirArreglo(lista);
		insertionSort(lista);
	}
	
	public static void insertionSort(int[] A) {
		int key;
		int i;
		for (int j=1; j<A.length; j=j+1) {
			key = A[j];
			//Insertar A[j] en la secuencia ordenada A[1..j-1]
			i=j-1;
			while(i>-1 && A[i]>key) {
				A[i+1] = A[i];
				i = i-1;
			}
			imprimirArreglo(A);
			A[i+1] = key;
		}		
	}
	
	public static void imprimirArreglo(int[] lista){
		System.out.println("");
		for (int x=0; x<lista.length; x++) {
			System.out.print(lista[x] + " ");
		}
	}
}
