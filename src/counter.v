module counter (
    input wire enable,
    input wire clk_in,
    input wire load,
    input wire up_down,
    input wire [7:0] in,
    output reg [7:0] counter_reg,
    input wire clk,
    input wire rst_n     // reset_n - low to reset
);

    // Flip flops for input so that there is no metastability
    reg enable_ff1, enable_ff2, ff_enable;
    reg clk_in_ff1, clk_in_ff2, ff_clk_in;
    reg load_ff1, load_ff2, ff_load;
    reg up_down_ff1, up_down_ff2, ff_up_down;
    reg [7:0] in_ff1, in_ff2, ff_in;
    
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            // Reset all output counter registers to 0
            counter_reg <= 8'h00;
        end else begin
            // First flip flop values for inputs
            enable_ff1 <= enable;
            clk_in_ff1 <= clk_in;
            load_ff1 <= load;
            up_down_ff1 <= up_down;
            in_ff1 <= in;
            
            // Second flip flop values
            enable_ff2 <= enable_ff1;
            clk_in_ff2 <= clk_in_ff1;
            load_ff2 <= load_ff1;
            up_down_ff2 <= up_down_ff1;
            in_ff2 <= in_ff1;

            // Stable input values held long enough by the flip flops
            ff_enable <= enable_ff2;
            ff_clk_in <= clk_in_ff2;
            ff_load <= load_ff2;
            ff_up_down <= up_down_ff2;
            ff_in <= in_ff2;

            // At every positive ff_sclk edge, update the counter
            if (ff_enable && enable_ff2) begin
                $display("Enable");
                if (!ff_load && load_ff2) begin
                    $display("Load");
                    counter_reg <= in;
                end else if (!ff_clk_in && clk_in_ff2) begin
                    
                    $display("Clk_in rising edge");
                    if (ff_up_down) begin
                        counter_reg <= counter_reg + 1;
                        $display("Increase count");
                    end else begin
                        counter_reg <= counter_reg - 1;
                        $display("Decrease count");
                    end
                end
            end
        end
    end

endmodule