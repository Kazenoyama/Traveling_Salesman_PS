import java.lang.reflect.Array;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;

public class Instance {

    public Instance(){
        
    }

    public ArrayList<String> readLine(String filePath){
        ArrayList<String> lines = new ArrayList<>();
        try(BufferedReader reader = new BufferedReader(new FileReader(filePath))){
            String line = reader.readLine();
            line = reader.readLine(); // Skip the first line
            while(line != null){
                lines.add(line);
                line = reader.readLine();
            }
        }catch(IOException e){
            e.printStackTrace();
        }
        return lines;
    }

    public void writeOutput(ArrayList<String> output, String filePath){

        Path path = Paths.get(filePath).getParent();
        if (path != null) {
            try {
                Files.createDirectories(path); // Create directories if they don't exist
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
        
        try(BufferedWriter writer = new BufferedWriter(new FileWriter(filePath))){
            writer.write(output.size() + "\n");
            for(String line : output){
                writer.write(line + "\n");
            }
        }catch(IOException e){
            e.printStackTrace();
        }
    }

    public ArrayList<String> randomChoosing(ArrayList<String> lines, int maximumArray){
        int random =(int) (Math.random() * lines.size());
        ArrayList<String> output = new ArrayList<>();
        for(int i = 0; i < maximumArray; i++){
            output.add(lines.get(random));
            lines.remove(random);
            random = (int) (Math.random() * lines.size());
        }
        return output;
    }

    public static void main(String[] args){

        int[] size = {100, 1000, 5000, 10000, 25000, 50000};
        int numberOfInstance = 10;

        Instance instance = new Instance();
        String filePath = "b_lovely_landscapes.txt";
        for(int i = 0; i < size.length; i++){
            for(int j = 0; j < numberOfInstance; j++){
                ArrayList<String> lines = instance.readLine(filePath);
                ArrayList<String> output = instance.randomChoosing(lines, size[i]);
                instance.writeOutput(output, "./b_instance/"+size[i]+"/instance_" + size[i] + "_number"+ j + ".txt");
            
            }
        }

        String filePath2 = "d_pet_pictures.txt";
        for(int i = 0; i < size.length; i++){
            for(int j = 0; j < numberOfInstance; j++){
                ArrayList<String> lines = instance.readLine(filePath2);
                ArrayList<String> output = instance.randomChoosing(lines, size[i]);
                instance.writeOutput(output, "./d_instance/"+size[i]+"/instance_" + size[i] + "_number"+ j + ".txt");
            
            }
        }

        String filePath3 = "e_shiny_selfies.txt";
        for(int i = 0; i < size.length; i++){
            for(int j = 0; j < numberOfInstance; j++){
                ArrayList<String> lines = instance.readLine(filePath3);
                ArrayList<String> output = instance.randomChoosing(lines, size[i]);
                instance.writeOutput(output, "./e_instance/"+size[i]+"/instance_" + size[i] + "_number"+ j + ".txt");
            
            }
        }

    }
    
    
}
