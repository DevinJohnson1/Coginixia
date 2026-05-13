package simple;

public class FindMax {
    public static void main(String[] args) {
        int[] arr = new int[3];
        System.out.println(arr.length);
        arr[0] = 10;
        arr[1] = 20;
        arr[2] = 30;
        System.out.println(arr.length);

        int[] nums = {10,0,-2,50,23}; //50 is the maximum
        System.out.println(nums.length);
        int max = findMax(nums);
        System.out.println("Max is: " + max);
    }
    private static int findMax(int[] nums){
        int max = nums[0];
        for(int i=1; i<nums.length; i++){
            if(nums[i] > max){
                max = nums[i];
            }
        }
        return max;
    }
}