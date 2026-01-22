---
name: transformer-block
description: Transformer architecture and block visualization
metadata:
  tags: transformer, architecture, encoder, decoder
---

# Transformer Block Visualization

## Transformer Block Structure

```python
from manim import *

class TransformerBlock(Scene):
    def construct(self):
        title = Text("Transformer Block", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))

        # Build transformer block components
        block = self.create_transformer_block()
        block.scale(0.9)

        self.play(Create(block), run_time=2)
        self.wait()

    def create_transformer_block(self):
        components = VGroup()

        # Input
        input_box = Rectangle(width=2, height=0.5, fill_color=BLUE, fill_opacity=0.5)
        input_label = Text("Input", font_size=16).move_to(input_box)
        components.add(VGroup(input_box, input_label))

        # Multi-Head Attention
        mha = Rectangle(width=3, height=0.8, fill_color=ORANGE, fill_opacity=0.6)
        mha_label = Text("Multi-Head Attention", font_size=14).move_to(mha)
        mha.next_to(input_box, UP, buff=0.5)
        mha_label.move_to(mha)
        components.add(VGroup(mha, mha_label))

        # Add & Norm 1
        add_norm1 = Rectangle(width=2.5, height=0.5, fill_color=TEAL, fill_opacity=0.5)
        add_norm1_label = Text("Add & Norm", font_size=12).move_to(add_norm1)
        add_norm1.next_to(mha, UP, buff=0.3)
        add_norm1_label.move_to(add_norm1)
        components.add(VGroup(add_norm1, add_norm1_label))

        # Feed Forward
        ff = Rectangle(width=3, height=0.8, fill_color=PURPLE, fill_opacity=0.6)
        ff_label = Text("Feed Forward", font_size=14).move_to(ff)
        ff.next_to(add_norm1, UP, buff=0.5)
        ff_label.move_to(ff)
        components.add(VGroup(ff, ff_label))

        # Add & Norm 2
        add_norm2 = Rectangle(width=2.5, height=0.5, fill_color=TEAL, fill_opacity=0.5)
        add_norm2_label = Text("Add & Norm", font_size=12).move_to(add_norm2)
        add_norm2.next_to(ff, UP, buff=0.3)
        add_norm2_label.move_to(add_norm2)
        components.add(VGroup(add_norm2, add_norm2_label))

        # Output
        output_box = Rectangle(width=2, height=0.5, fill_color=GREEN, fill_opacity=0.5)
        output_label = Text("Output", font_size=16).move_to(output_box)
        output_box.next_to(add_norm2, UP, buff=0.5)
        output_label.move_to(output_box)
        components.add(VGroup(output_box, output_label))

        # Arrows
        arrows = VGroup()
        for i in range(len(components) - 1):
            arrow = Arrow(
                components[i].get_top(),
                components[i + 1].get_bottom(),
                buff=0.1,
                color=WHITE
            )
            arrows.add(arrow)
        components.add(arrows)

        # Residual connections
        residual1 = CurvedArrow(
            input_box.get_right() + RIGHT * 0.2,
            add_norm1.get_right() + RIGHT * 0.2,
            angle=-TAU/4,
            color=YELLOW
        )
        residual2 = CurvedArrow(
            add_norm1.get_right() + RIGHT * 0.5,
            add_norm2.get_right() + RIGHT * 0.5,
            angle=-TAU/4,
            color=YELLOW
        )
        components.add(residual1, residual2)

        return components
```

## Full Transformer Architecture

```python
class FullTransformerArchitecture(Scene):
    def construct(self):
        title = Text("Transformer Architecture", font_size=32)
        title.to_edge(UP)
        self.play(Write(title))

        # Encoder stack
        encoder = self.create_stack("Encoder", 3, BLUE)
        encoder.shift(LEFT * 3)

        # Decoder stack
        decoder = self.create_stack("Decoder", 3, GREEN)
        decoder.shift(RIGHT * 3)

        # Input/Output embeddings
        input_emb = Rectangle(width=2, height=0.5, fill_color=GRAY, fill_opacity=0.5)
        input_emb_label = Text("Input\nEmbedding", font_size=12).move_to(input_emb)
        input_emb.next_to(encoder, DOWN, buff=0.5)
        input_emb_label.move_to(input_emb)

        output_emb = Rectangle(width=2, height=0.5, fill_color=GRAY, fill_opacity=0.5)
        output_emb_label = Text("Output\nEmbedding", font_size=12).move_to(output_emb)
        output_emb.next_to(decoder, DOWN, buff=0.5)
        output_emb_label.move_to(output_emb)

        # Positional encoding
        pos_enc1 = Text("+ Positional Encoding", font_size=10, color=YELLOW)
        pos_enc1.next_to(input_emb, DOWN, buff=0.1)
        pos_enc2 = Text("+ Positional Encoding", font_size=10, color=YELLOW)
        pos_enc2.next_to(output_emb, DOWN, buff=0.1)

        # Cross-attention arrow
        cross_arrow = Arrow(
            encoder.get_right(),
            decoder.get_left(),
            color=ORANGE
        )
        cross_label = Text("Cross-Attention", font_size=12, color=ORANGE)
        cross_label.next_to(cross_arrow, UP, buff=0.1)

        # Final output
        final_output = Rectangle(width=2, height=0.5, fill_color=RED, fill_opacity=0.5)
        final_label = Text("Output\nProbabilities", font_size=10).move_to(final_output)
        final_output.next_to(decoder, UP, buff=0.5)
        final_label.move_to(final_output)

        # Animate
        self.play(Create(encoder), Create(decoder))
        self.play(
            Create(VGroup(input_emb, input_emb_label)),
            Create(VGroup(output_emb, output_emb_label))
        )
        self.play(Write(pos_enc1), Write(pos_enc2))
        self.play(GrowArrow(cross_arrow), Write(cross_label))
        self.play(Create(VGroup(final_output, final_label)))
        self.wait()

    def create_stack(self, name, n_layers, color):
        stack = VGroup()
        for i in range(n_layers):
            block = Rectangle(
                width=2.5,
                height=0.8,
                fill_color=color,
                fill_opacity=0.4 + 0.2 * (i / n_layers)
            )
            block_label = Text(f"{name} {i+1}", font_size=12)
            block_label.move_to(block)
            layer = VGroup(block, block_label)
            stack.add(layer)

        stack.arrange(UP, buff=0.2)

        # Stack label
        label = Text(f"{name}\nStack", font_size=14, color=color)
        label.next_to(stack, DOWN, buff=0.3)
        stack.add(label)

        return stack
```

## Encoder Block Detail

```python
class EncoderBlockDetail(Scene):
    def construct(self):
        title = Text("Encoder Block", font_size=32)
        title.to_edge(UP)

        # Components with internal detail
        self.play(Write(title))

        # Self-attention sublayer
        sa_box = RoundedRectangle(
            width=4, height=1.5,
            corner_radius=0.2,
            fill_color=ORANGE,
            fill_opacity=0.3
        )
        sa_label = Text("Self-Attention", font_size=16)

        # Q, K, V inside
        qkv = VGroup(
            Rectangle(width=0.8, height=0.5, fill_color=RED, fill_opacity=0.5),
            Rectangle(width=0.8, height=0.5, fill_color=GREEN, fill_opacity=0.5),
            Rectangle(width=0.8, height=0.5, fill_color=BLUE, fill_opacity=0.5),
        )
        qkv.arrange(RIGHT, buff=0.2)

        qkv_labels = VGroup(
            Text("Q", font_size=12),
            Text("K", font_size=12),
            Text("V", font_size=12),
        )
        for label, box in zip(qkv_labels, qkv):
            label.move_to(box)

        sa_content = VGroup(sa_label, qkv, qkv_labels)
        sa_content.arrange(DOWN, buff=0.2)
        sa_content.move_to(sa_box)

        sa_group = VGroup(sa_box, sa_content)
        sa_group.shift(DOWN * 1)

        self.play(Create(sa_group))

        # Feed-forward sublayer
        ff_box = RoundedRectangle(
            width=4, height=1.2,
            corner_radius=0.2,
            fill_color=PURPLE,
            fill_opacity=0.3
        )
        ff_box.next_to(sa_box, UP, buff=1)

        ff_content = VGroup(
            Text("Feed Forward", font_size=16),
            MathTex(r"FFN(x) = ReLU(xW_1)W_2", font_size=20)
        )
        ff_content.arrange(DOWN, buff=0.2)
        ff_content.move_to(ff_box)

        ff_group = VGroup(ff_box, ff_content)

        self.play(Create(ff_group))

        # Layer normalization and residual
        add_norm1 = self.create_add_norm()
        add_norm1.next_to(sa_box, UP, buff=0.3)

        add_norm2 = self.create_add_norm()
        add_norm2.next_to(ff_box, UP, buff=0.3)

        self.play(Create(add_norm1), Create(add_norm2))
        self.wait()

    def create_add_norm(self):
        box = Rectangle(width=2, height=0.4, fill_color=TEAL, fill_opacity=0.5)
        label = Text("Add & Norm", font_size=10).move_to(box)
        return VGroup(box, label)
```

## Guidelines

- Use consistent colors: attention (orange), FFN (purple), normalization (teal)
- Show residual connections as curved arrows
- Stack encoder/decoder blocks vertically
- Animate layer-by-layer to explain data flow
- Include cross-attention between encoder and decoder

## Forbidden

- Do NOT overcrowd with all internal details at once
- Do NOT forget residual connections (key concept)
- Do NOT use same color for different components
- Do NOT skip layer normalization visualization
